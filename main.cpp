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

        static constexpr DWORD64 MAX_ADDRESS = 0xFFFFFFFF;
        static constexpr DWORD64 BASE_ADDRESS = 0xF0000000;

        // On Bike AoB -------------------------------- 233,    2,   32,   63,   13,   25,    0,    0,    0,    0,    0,    2,    0,    0,    0
        static constexpr uint8_t BK_AOB_LEN = 15u;
        static constexpr uint8_t BK_AOB[BK_AOB_LEN] = {0xE9, 0x02, 0x20, 0x3F, 0x0D, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00};

        // Off Bike AoB ----------------------------------- 233,    2,   32,   63,   13,   25,    0,    0,    0,    0,    0,    0,    0,    0,    0
        static constexpr uint8_t OFF_BK_AOB[BK_AOB_LEN] = {0xE9, 0x02, 0x20, 0x3F, 0x0D, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

        static DWORD64 getAddrAob(HWND hwnd, const uint8_t* aob, const uint8_t aobLen)
        {
            // Get process id
            DWORD pid;
            GetWindowThreadProcessId(hwnd, &pid);

            // Get process handle
            HANDLE phandle = OpenProcess(PROCESS_ALL_ACCESS, false, pid);

            // Read memory region
            uint32_t size = Util::MAX_ADDRESS - Util::BASE_ADDRESS;
            uint8_t* bytes = new uint8_t[size];
            ReadProcessMemory(phandle, (LPCVOID) Util::BASE_ADDRESS, bytes, size, NULL);

            for (uint32_t i = 0u; i < size; i++)
            {
                for (uint8_t j = 0u; j < aobLen; j++)
                {
                    BOOL match = aob[j] == bytes[i + j];

                    if (match)
                    {
                        if (j == aobLen - 1)
                        {
                            return Util::BASE_ADDRESS + i;
                        }

                    } else break;

                } // End of loop

            } // End of loop

            return 0;

        } // End of find op code bytes function

        static DWORD64 getBikeToggleAddr(HWND hwnd) //TODO: use ref
        {
            // TODO: If 0 toggle bike key, and search for bike address again
            // Need to be on bike first
            DWORD64 addr = Util::getAddrAob(hwnd, &BK_AOB[0], BK_AOB_LEN) + 11;
            return addr;
        }

}; // End of Util class


class Script
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

}; // End of Script class


int main()
{

    HWND hwnd = FindWindowA("GLFW30", NULL);

    //for (int i = 0; i < 0x00888888; i++)
    //{
    //    std::cout << i << std::endl;
    //}

    ////GetModuleBaseAddress(hwnd);
    //std::cout << "HANDLE: " << hwnd << std::endl;
    //Util::findOpCodeBytes(hwnd);
    DWORD64 addr = Util::getBikeToggleAddr(hwnd);

    while(TRUE)
    {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        Script::isOnBike(hwnd, addr);
    }


//    //// Get process id
//    DWORD pid;
//    GetWindowThreadProcessId(hwnd, &pid);
//
//    // Get process handle
//    HANDLE phandle = OpenProcess(PROCESS_ALL_ACCESS, false, pid);
//
//    DWORD64 maxAddress = 0xFFFFFFFF;
//    DWORD64 baseAddress = 0xF0000000;
//
//    //uint32_t size = 2'079'197;
//    uint32_t size = 268'435'455;
//    std::cout << size << std::endl;
//    uint8_t* memoryRegion = new uint8_t[size];
//    ReadProcessMemory(phandle, (LPCVOID) baseAddress, memoryRegion, size, NULL);
//
//    std::cout << (int) memoryRegion[42053065] << std::endl;
//
//    //for (int i = 0; i < size; i++)
//    //{
//    //    std::cout << (int) memoryRegion[i] << std::endl;
//    //}

//
//    constexpr auto BYTES_IN_AVX_REG = 32u;
//    uint8_t byteArray0[BYTES_IN_AVX_REG];
//    uint8_t byteArray1[BYTES_IN_AVX_REG];
//    uint8_t aob[15] = {0xE9, 0x02, 0x20, 0x3F, 0x0D, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00};
//
//    std::cout << "ALIGN: " << alignof(byteArray0) << std::endl;
//    std::cout << "ALIGN: " << alignof(byteArray1) << std::endl;
//
//    ReadProcessMemory(phandle, (LPCVOID) 0xF0000000, byteArray0, sizeof(byteArray0), NULL);
//    ReadProcessMemory(phandle, (LPCVOID) 0xF2450AE9, byteArray1, sizeof(byteArray1), NULL);
//
//    for (uint8_t byte : byteArray0)
//    {
//        std::cout << (int) byte << std::endl;
//    }
//    std::cout << "=====================" << std::endl;
//    //std::cout << "=====================" << std::endl;
//    //for (uint8_t byte : byteArray1)
//    //{
//    //    std::cout << (int) byte << std::endl;
//    //}
//    //std::cout << "=====================" << std::endl;
//
//    auto r0 = _mm256_load_si256((__m256i*) byteArray0);
//    auto r1 = _mm256_load_si256((__m256i*) byteArray1);
//    auto targetAob = _mm256_load_si256((__m256i*) aob);
//
//    auto r3 = _mm256_add_epi8(r0, r1);
//    auto r4 = _mm256_cmpeq_epi8(r0, targetAob);
//
//    //std::cout << _mm256_extract_epi8(r3, 0) << std::endl;
//
//    uint8_t* res = (uint8_t*) &r4;
//    for (int i = 0; i < 15; i++)
//    {
//        std::cout << (int) res[i] << std::endl;
//    }
//
//    uint8_t match = res[0] & res [1] & res [2] & res [3] & res [4] & res [5] & res [6] & res [7] & res [8] & res [9] & res [10] & res [11] & res [12] & res [13] & res [14];
//    std::cout << "match: " << (int) match << std::endl;




    //uintptr_t val;
    //uintptr_t addr = 0x7FF74D990000;
    //ReadProcessMemory(phandle, (LPCVOID) addr, &val, sizeof(val), NULL);
    //std::cout << "val: " << val << std::endl;


    //DWORD64 baseAddress = Util::getBaseAddress(hwnd);

    //if (baseAddress) std::cout << "Base address returned: " << baseAddress << std::endl;


    //std::cout << "Main base address: " << baseAddress << std::endl;

    //SetForegroundWindow(hwnd);

    //for (int i = 0; i < 3; i++)
    //{
    //    Script::run(Keys::RIGHT, 4);
    //    Script::run(Keys::DOWN, 2);
    //    Script::run(Keys::LEFT, 4);
    //    Script::run(Keys::UP, 2);
    //}


    return 0;
}
