#include "BS_thread_pool.hpp"

#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include <Windows.h>
#include <Psapi.h>


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

        // Bike
        static constexpr uint8_t BK_ADDR_OFFSET = 11u;
        static constexpr uint8_t BK_AOB_LEN = 15u;
        // On Bike AoB -------------------------------- 233,    2,   32,   63,   13,   25,    0,    0,    0,    0,    0,    2,    0,    0,    0
        static constexpr uint8_t BK_AOB[BK_AOB_LEN] = {0xE9, 0x02, 0x20, 0x3F, 0x0D, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00};
        // Off Bike AoB ----------------------------------- 233,    2,   32,   63,   13,   25,    0,    0,    0,    0,    0,    0,    0,    0,    0
        static constexpr uint8_t OFF_BK_AOB[BK_AOB_LEN] = {0xE9, 0x02, 0x20, 0x3F, 0x0D, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

        static constexpr uint8_t THREADS = 8;

        static DWORD64 getAddrAob(const HANDLE& phandle, const uint8_t (&aob)[], const uint8_t& aobLen, BS::thread_pool* tpool = 0)
        {
            auto fn = [](const DWORD64 baseAddress,
                         const HANDLE& phandle,
                         const uint32_t& size,
                         const uint8_t (&aob)[], const uint8_t& aobLen) -> DWORD64
            {
                uint8_t* bytes = new uint8_t[size];
                ReadProcessMemory(phandle, (LPCVOID) baseAddress, bytes, size, NULL);

                for (uint32_t i = 0u; i < size; i++)
                {
                    for (uint8_t j = 0u; j < aobLen; j++)
                    {
                        if (aob[j] == bytes[i + j])
                        {
                            if (j == aobLen - 1)
                            {
                                delete[] bytes;
                                return baseAddress + i;
                            }

                        } else break;

                    } // End of loop

                } // End of loop

                delete[] bytes;
                return 0;

            }; // End of fn

            if (tpool)
            {
                uint32_t addrOffset = std::ceil((double) Util::ADDRESS_COUNT_32b / Util::THREADS);
                DWORD64 baseAddr;

                auto future0 = tpool->submit(fn, std::ref(Util::BASE_ADDRESS_32b), std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                baseAddr = Util::BASE_ADDRESS_32b + addrOffset;
                auto future1 = tpool->submit(fn, baseAddr, std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                baseAddr = Util::BASE_ADDRESS_32b + (addrOffset * 2);
                auto future2 = tpool->submit(fn, std::ref(baseAddr), std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                baseAddr = Util::BASE_ADDRESS_32b + (addrOffset * 3);
                auto future3 = tpool->submit(fn, std::ref(baseAddr), std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                baseAddr = Util::BASE_ADDRESS_32b + (addrOffset * 4);
                auto future4 = tpool->submit(fn, std::ref(baseAddr), std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                baseAddr = Util::BASE_ADDRESS_32b + (addrOffset * 5);
                auto future5 = tpool->submit(fn, std::ref(baseAddr), std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                baseAddr = Util::BASE_ADDRESS_32b + (addrOffset * 6);
                auto future6 = tpool->submit(fn, std::ref(baseAddr), std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                baseAddr = Util::BASE_ADDRESS_32b + (addrOffset * 7);
                auto future7 = tpool->submit(fn, std::ref(baseAddr), std::ref(phandle), std::ref(addrOffset), std::ref(aob), std::ref(aobLen));

                //future0.wait();
                future1.wait();
                return future1.get();
                //future2.wait();
                //future3.wait();
                //future4.wait();
                //future5.wait();
                //future6.wait();
                //future7.wait();

                //if (future0.get() > 0) return future0.get();
                //if (future2.get() > 0) return future2.get();
                //if (future3.get() > 0) return future3.get();
                //if (future4.get() > 0) return future4.get();
                //if (future5.get() > 0) return future5.get();
                //if (future6.get() > 0) return future6.get();
                //if (future7.get() > 0) return future7.get();

            } else
            {
                return fn(Util::BASE_ADDRESS_32b, phandle, Util::ADDRESS_COUNT_32b, aob, aobLen);
            }

            return 0;

        } // End of find op code bytes function

        //static DWORD64 getBikeToggleAddr(const HANDLE& phandle)
        //{
        //    // TODO: If 0 toggle bike key, and search for bike address again
        //    // Need to be on bike first
        //    DWORD64 addr = Util::getAddrAob(phandle, BK_AOB, BK_AOB_LEN) + Util::BK_ADDR_OFFSET;
        //    return addr;
        //}

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

        //static BOOL isOnBike(HWND hwnd, DWORD64 addr)
        //{
        //    // Get process id
        //    DWORD pid;
        //    GetWindowThreadProcessId(hwnd, &pid);

        //    // Read value at memory address for biking
        //    int readValue;
        //    HANDLE phandle = OpenProcess(PROCESS_ALL_ACCESS, false, pid);
        //    ReadProcessMemory(phandle, (LPCVOID) addr, &readValue, sizeof(readValue), NULL);

        //    BOOL isOnBike = readValue == 2;

        //    std::cout << "Is on bike: " << isOnBike << std::endl;

        //    return isOnBike;
        //}

}; // End of Bot class


int main()
{
    // Start thread pool
    BS::thread_pool tpool(Util::THREADS);

    // Get handle to window
    HWND hwnd = FindWindowA("GLFW30", NULL);

    // Get process id
    DWORD pid;
    GetWindowThreadProcessId(hwnd, &pid);

    // Get process handle
    HANDLE phandle = OpenProcess(PROCESS_ALL_ACCESS, false, pid);

    auto start = std::chrono::high_resolution_clock::now();
    DWORD64 addr0 = Util::getAddrAob(phandle, Util::BK_AOB, Util::BK_AOB_LEN, &tpool);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "MT: " << addr0 << std::endl;
    std::cout << "MT: " << duration << std::endl;

    start = std::chrono::high_resolution_clock::now();
    DWORD64 addr1 = Util::getAddrAob(phandle, Util::BK_AOB, Util::BK_AOB_LEN);
    end = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Non-MT: " << addr1 << std::endl;
    std::cout << "Non-MT: " << duration << std::endl;


    //auto fn = [](int& i)
    //{
    //    std::cout << "TEST: " << i << std::endl;
    //};

    //int p = 0;
    //auto future = tpool.submit(fn, std::ref(p));

    //std::cout << (uint32_t) std::ceil((double) 268435455 / 8) << std::endl;

    //while(TRUE)
    //{
    //    std::this_thread::sleep_for(std::chrono::seconds(1));
    //    Bot::isOnBike(hwnd, addr);
    //}

    //for (int i = 0; i < 3; i++)
    //{
    //    Bot::run(Keys::RIGHT, 4);
    //    Bot::run(Keys::DOWN, 2);
    //    Bot::run(Keys::LEFT, 4);
    //    Bot::run(Keys::UP, 2);
    //}


    return 0;
}
