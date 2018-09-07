// prime calculation
#include <math.h>
#include <cstdint>

extern "C" {
__declspec(dllexport) bool cpp_is_prime(uint_fast32_t target);
}
bool cpp_is_prime(uint_fast32_t target){
    if(target < 2){
        return false;
    }
    else if(target == 2){
        return true;
    }
    else{
        for(int iter = 2; iter < static_cast<uint_fast32_t>(ceil(sqrt(target)) + 1); iter++){
            if (target % iter == 0){
                return false;
            }
        }
    }
    return true;
}
