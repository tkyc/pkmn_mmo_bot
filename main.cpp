#include "BS_thread_pool.hpp"

#include <iostream>
#include <Windows.h>
#include <Psapi.h>
#include <chrono>
#include <thread>
#include <immintrin.h>


#define BUFFER_SIZE 1024


static void listHwnds()
{
    EnumWindows([](HWND hwnd, LPARAM lparam)
    {
        // Buffer for window title
        char* buf = new char[BUFFER_SIZE];

        // Set buffer with window title
        GetWindowTextA(hwnd, buf, BUFFER_SIZE);

        // Print window titles if window is visible and window title exists
        if (IsWindowVisible(hwnd) && buf[0] > 0) std::cout << buf << std::endl;

        return TRUE;
    }, 0);

} // End of list hwnds function


enum Keys
{
    // WASD
    LEFT = 0x41,
    RIGHT = 0x44,
    UP = 0x57,
    DOWN = 0x53,

    // A & B
    A = 0x4a,
    B = 0x4b

}; // End of keys enum


class Util
{
    public:

        // Base address details
        static constexpr DWORD64 BASE_ADDRESS_32b = 0xF0000000;
        static constexpr DWORD64 MAX_ADDRESS_32b = 0xFFFFFFFF;
        static constexpr uint32_t ADDRESS_COUNT_32b = Util::MAX_ADDRESS_32b - Util::BASE_ADDRESS_32b;

        // On Bike AoB -------------------------------- 233,    2,   32,   63,   13,   25,    0,    0,    0,    0,    0,    2,    0,    0,    0
        static constexpr uint8_t BK_ADDR_OFFSET = 11u;
        static constexpr uint8_t BK_AOB_LEN = 15u;
        static constexpr uint8_t BK_AOB[BK_AOB_LEN] = {0xE9, 0x02, 0x20, 0x3F, 0x0D, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00};
        // Off Bike AoB ----------------------------------- 233,    2,   32,   63,   13,   25,    0,    0,    0,    0,    0,    0,    0,    0,    0
        static constexpr uint8_t OFF_BK_AOB[BK_AOB_LEN] = {0xE9, 0x02, 0x20, 0x3F, 0x0D, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

        static DWORD64 getAddrAob(const HANDLE& phandle, const uint8_t (&aob)[BK_AOB_LEN], const uint8_t& aobLen)
        {
            // Read memory region
            uint8_t* bytes = new uint8_t[Util::ADDRESS_COUNT_32b];
            ReadProcessMemory(phandle, (LPCVOID) Util::BASE_ADDRESS_32b, bytes, Util::ADDRESS_COUNT_32b, NULL);

            for (uint32_t i = 0u; i < Util::ADDRESS_COUNT_32b; i++)
            {
                for (uint8_t j = 0u; j < aobLen; j++)
                {
                    if (aob[j] == bytes[i + j])
                    {
                        if (j == aobLen - 1)
                        {
                            delete[] bytes;
                            return Util::BASE_ADDRESS_32b + i;
                        }

                    } else break;

                } // End of loop

            } // End of loop

            delete[] bytes;
            return 0;

        } // End of find op code bytes function

        static DWORD64 getBikeToggleAddr(const HANDLE& phandle)
        {
            // TODO: If 0 toggle bike key, and search for bike address again
            // Need to be on bike first
            DWORD64 addr = Util::getAddrAob(phandle, BK_AOB, BK_AOB_LEN) + Util::BK_ADDR_OFFSET;
            return addr;
        }

}; // End of Util class


class Bot
{
    public:

        static void walk(Keys key, int steps)
        {
            for (int i = 0; i < steps; i++)
            {
                // Key down
                keybd_event(key, 0, 0, 0);
                std::this_thread::sleep_for(std::chrono::milliseconds(200));

                // Key release
                keybd_event(key, 0, KEYEVENTF_KEYUP, 0);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }

        } // End of walk function

        static void run(Keys key, int steps)
        {
            // Hold run key
            keybd_event(Keys::B, 0, 0, 0);

            for (int i = 0; i < steps; i++)
            {
                // Key down
                keybd_event(key, 0, 0, 0);
                std::this_thread::sleep_for(std::chrono::milliseconds(150));

                // Key release
                keybd_event(key, 0, KEYEVENTF_KEYUP, 0);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }

            // Release run key
            keybd_event(Keys::B, 0, KEYEVENTF_KEYUP, 0);

        } // End of run function

        static void bike(Keys key, int steps)
        {
            // Hold run key
            keybd_event(Keys::B, 0, 0, 0);

            for (int i = 0; i < steps; i++)
            {
                // Key down
                keybd_event(key, 0, 0, 0);
                std::this_thread::sleep_for(std::chrono::milliseconds(150));

                // Key release
                keybd_event(key, 0, KEYEVENTF_KEYUP, 0);
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }

            // Release run key
            keybd_event(Keys::B, 0, KEYEVENTF_KEYUP, 0);

        } // End of run function

        static BOOL isOnBike(HWND hwnd, DWORD64 addr)
        {
            // Get process id
            DWORD pid;
            GetWindowThreadProcessId(hwnd, &pid);

            // Read value at memory address for biking
            int readValue;
            HANDLE phandle = OpenProcess(PROCESS_ALL_ACCESS, false, pid);
            ReadProcessMemory(phandle, (LPCVOID) addr, &readValue, sizeof(readValue), NULL);

            BOOL isOnBike = readValue == 2;

            std::cout << "Is on bike: " << isOnBike << std::endl;

            return isOnBike;
        }

}; // End of Bot class


int main()
{
    // Get handle to window
    HWND hwnd = FindWindowA("GLFW30", NULL);

    // Get process id
    DWORD pid;
    GetWindowThreadProcessId(hwnd, &pid);

    // Get process handle
    HANDLE phandle = OpenProcess(PROCESS_ALL_ACCESS, false, pid);

    //Util::findOpCodeBytes(hwnd);
    DWORD64 addr = Util::getAddrAob(phandle, Util::BK_AOB, Util::BK_AOB_LEN);
    //DWORD64 addr = Util::getBikeToggleAddr(phandle);
    std::cout << addr << std::endl;

    //while(TRUE)
    //{
    //    std::this_thread::sleep_for(std::chrono::seconds(1));
    //    Bot::isOnBike(hwnd, addr);
    //}

    return 0;
}
