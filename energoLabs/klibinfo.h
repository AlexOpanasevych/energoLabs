#ifndef KLIBINFO_H
#define KLIBINFO_H

#include <QQmlEngine>
//#include <klibcorelite_global.h>
#define USE_KLIBCORE_AS_SUBPROJECT

class KLibInfo {
    static const int static_call;
public:
    static inline const char *libname = "KLib";
    static inline const int major = 1;
    static inline const int minor = 0;
};


template<typename T>
struct KCompareEngine {
    static bool compare(const T &arg0, const T &arg1) {
        if constexpr(std::is_same<T, QJSValue>::value) {
            return false;
        } else {
            return arg0 == arg1;
        }
    }
};

template<>
struct KCompareEngine<double> {
    static bool compare(double arg0, double arg1) {
        return qFuzzyCompare(arg0, arg1);
    }
};

template<>
struct KCompareEngine<float> {
    static bool compare(float arg0, float arg1) {
        return qFuzzyCompare(arg0, arg1);
    }
};


#endif // KLIBINFO_H
