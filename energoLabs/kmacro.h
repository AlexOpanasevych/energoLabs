#pragma once
//See Gist Comment for description, usage, warnings and license information

//#include "kclassregistry.h"
#include <QQmlApplicationEngine>
#include <QDataStream>
#include <QFile>
#include "klibinfo.h"


#define K_EXPAND(BLOCK) QVector<int> { 0, ((void)(BLOCK), 0) ... };

#define K_AUTO_PROPERTY(TYPE, NAME, GETTER, SETTER, NOTIFIER, DEFAULT) \
Q_PROPERTY(TYPE NAME READ GETTER WRITE SETTER NOTIFY NOTIFIER) \
public: \
    TYPE GETTER() const { return this->m_ ## NAME; } \
    void SETTER(TYPE value) { \
        if (KCompareEngine<TYPE>::compare(this->m_ ## NAME, value)) return; \
        this->m_ ## NAME = value; \
        emit NOTIFIER(value); \
    } \
    Q_SIGNAL void NOTIFIER(TYPE value); \
private: \
    TYPE m_ ## NAME = DEFAULT;

#define K_CONST_PROPERTY(TYPE, NAME, DEFAULT) \
Q_PROPERTY(TYPE NAME READ NAME NOTIFY NAME ## Changed) \
public: \
    TYPE NAME() const { return this->m_ ## NAME; } \
    Q_SIGNAL void NAME ## Changed(TYPE value); \
private: \
    TYPE m_ ## NAME = DEFAULT;


#define K_READONLY_PROPERTY(TYPE, NAME, GETTER, SETTER, NOTIFIER, DEFAULT) \
Q_PROPERTY(TYPE NAME READ GETTER NOTIFY NOTIFIER) \
public: \
    TYPE GETTER() const { return this->m_ ## NAME; } \
    Q_SIGNAL void NOTIFIER(TYPE value); \
private: \
    TYPE m_ ## NAME = DEFAULT; \
    void SETTER(TYPE value) { \
        if (KCompareEngine<TYPE>::compare(this->m_ ## NAME, value)) return; \
        this->m_ ## NAME = value; \
        emit NOTIFIER(value); \
    }

#define K_PROTECTED_PROPERTY(TYPE, NAME, GETTER, SETTER, NOTIFIER, DEFAULT) \
Q_PROPERTY(TYPE NAME READ GETTER NOTIFY NOTIFIER) \
public: \
    TYPE GETTER() const { return this->m_ ## NAME; } \
    Q_SIGNAL void NOTIFIER(TYPE value); \
protected: \
    TYPE m_ ## NAME = DEFAULT; \
    void SETTER(TYPE value) { \
        if (KCompareEngine<TYPE>::compare(this->m_ ## NAME, value)) return; \
        this->m_ ## NAME = value; \
        emit NOTIFIER(value); \
    }



#define K_AUTO_MEMBER(TYPE, NAME, GETTER, SETTER, DEFAULT) \
public: \
    TYPE GETTER() const { return this->m_ ## NAME; } \
    void SETTER(TYPE value) { \
        this->m_ ## NAME = value; \
    } \
private: \
    TYPE m_ ## NAME = DEFAULT;

#define K_CONST_MEMBER(TYPE, NAME, DEFAULT) \
public: \
    TYPE NAME() const { return this->m_ ## NAME; } \
private: \
    TYPE m_ ## NAME = DEFAULT;


#define K_READONLY_MEMBER(TYPE, NAME, GETTER, SETTER, DEFAULT) \
public: \
    TYPE GETTER() const { return this->m_ ## NAME; } \
private: \
    TYPE m_ ## NAME = DEFAULT; \
    void SETTER(TYPE value) { \
        this->m_ ## NAME = value; \
    }

#define K_PROTECTED_MEMBER(TYPE, NAME, GETTER, SETTER, DEFAULT) \
public: \
    TYPE GETTER() const { return this->m_ ## NAME; } \
protected: \
    TYPE m_ ## NAME = DEFAULT; \
    void SETTER(TYPE value) { \
        this->m_ ## NAME = value; \
    }



#define K_GENERATE_METHOD_CHECKER(METHOD_NAME) \
template <typename T> \
class k_has_ ## METHOD_NAME ## _method { \
private: \
    typedef char YesType[1]; \
    typedef char NoType[2]; \
    template <typename C> static YesType& test( decltype(&C:: METHOD_NAME) ) ; \
    template <typename C> static NoType& test(...); \
public: \
    enum { value = sizeof(test<T>(0)) == sizeof(YesType) }; \
};

K_GENERATE_METHOD_CHECKER(push_back)
K_GENERATE_METHOD_CHECKER(append)
K_GENERATE_METHOD_CHECKER(clear)

template <typename ContainerType, typename ItemType>
void kAppendToContainer(ContainerType *container, ItemType item) {
    if constexpr(k_has_push_back_method<ContainerType>::value) { \
        container->push_back(item);
    } else if constexpr(k_has_append_method<ContainerType>::value) {
        container->append(item);
    }
}

#define K_LIST_PROPERTY(TYPE, NAME, CONTAINER) \
private: \
    Q_PROPERTY(QQmlListProperty<TYPE> NAME READ NAME NOTIFY NAME ## Changed) \
public: \
    Q_SIGNAL void NAME ## Changed(QQmlListProperty<TYPE>); \
    Q_INVOKABLE QQmlListProperty<TYPE> NAME() { \
        typedef std::remove_pointer<decltype (this)>::type THIS_TYPE; \
        typedef std::remove_pointer<decltype (CONTAINER)>::type CONTAINER_TYPE; \
        auto size = [](QQmlListProperty<TYPE>* list){ return reinterpret_cast<THIS_TYPE*>(list->data)->CONTAINER.size(); }; \
        auto element = [](QQmlListProperty<TYPE>* list, int index) -> TYPE* { auto container = reinterpret_cast<THIS_TYPE*>(list->data)->CONTAINER; \
            int i = 0; \
            for(auto item : container) { \
                if(i == index) { \
                    return item; \
                } \
                i++; \
            } \
            return nullptr; \
        }; \
        if constexpr(k_has_push_back_method<CONTAINER_TYPE>::value and k_has_clear_method<CONTAINER_TYPE>::value) { \
            auto append = [](QQmlListProperty<TYPE>* list, TYPE* p) { \
                kAppendToContainer(&reinterpret_cast<THIS_TYPE*>(list->data)->CONTAINER, p); \
            }; \
            auto clear = [](QQmlListProperty<TYPE>* list) { reinterpret_cast<THIS_TYPE*>(list->data)->CONTAINER.clear(); }; \
            return QQmlListProperty<TYPE>(this, this, append, size, element, clear); \
        } else { \
            return QQmlListProperty<TYPE>(this, this, size, element); \
        } \
    }


#define K_READONLY_LIST_PROPERTY(TYPE, NAME, CONTAINER) \
private: \
    Q_PROPERTY(QQmlListProperty<TYPE> NAME READ NAME NOTIFY NAME ## Changed) \
public: \
    Q_SIGNAL void NAME ## Changed(QQmlListProperty<TYPE>); \
    Q_INVOKABLE QQmlListProperty<TYPE> NAME() { \
        typedef std::remove_pointer<decltype (this)>::type THIS_TYPE; \
        auto size = [](QQmlListProperty<TYPE>* list){ return reinterpret_cast<THIS_TYPE*>(list->data)->CONTAINER.size(); }; \
        auto element = [](QQmlListProperty<TYPE>* list, int index) -> TYPE* { auto container = reinterpret_cast<THIS_TYPE*>(list->data)->CONTAINER; \
            int i = 0; \
            for(auto item : container) { \
                if(i == index) { \
                    return item; \
                } \
                i++; \
            } \
            return nullptr; \
        }; \
        return QQmlListProperty<TYPE>(this, this, size, element); \
    }

#define K_SINGLETON(TYPE) \
public: \
    static TYPE *instance() { \
        static TYPE *m_instance; \
        if (m_instance == nullptr) { \
            m_instance = new TYPE(); \
        } \
        return m_instance; \
    } \
private:


#define K_PRIVATE_SINGLETON(TYPE) \
private: \
    static TYPE *instance() { \
        static TYPE *m_instance; \
        if (m_instance == nullptr) { \
            m_instance = new TYPE(); \
        } \
        return m_instance; \
    }


#define K_ERROR_STRING() \
    K_PROTECTED_PROPERTY(QString, errorString, errorString, setErrorString, errorStringChanged, "")

#define K_DISPLAY_ERROR(CONDITION, TEXT) \
    if(CONDITION) { \
        setErrorString(TEXT); \
        return; \
    } else { \
        setErrorString(""); \
    }


#ifdef KLIBCORE_USE_EXTENDED_META_SYSTEM
    #define __K_EXTENDED_TYPE_REGISTRATION(TYPE) \
    private: \
        static inline const QString TYPE ## MetaTypeName = KClassRegistry::registerType<TYPE>();

    #define K_QML_TYPE(TYPE) \
    __K_EXTENDED_TYPE_REGISTRATION(TYPE) \
        static inline const int TYPE ## QMLRegistration = qmlRegisterType<TYPE>(KLibInfo::libname, KLibInfo::major, KLibInfo::minor, # TYPE);
    #define K_META_TYPE_EXTENDED(TYPE) \
    __K_EXTENDED_TYPE_REGISTRATION(TYPE) \
        static inline const int TYPE ## MetaRegistration = qRegisterMetaType<TYPE>();
#else
    #define K_QML_TYPE(TYPE) \
    private: \
        static inline const int TYPE ## QMLRegistration = qmlRegisterType<TYPE>(KLibInfo::libname, KLibInfo::major, KLibInfo::minor, # TYPE);
#endif

#define K_META_TYPE(TYPE) \
private: \
    static inline const int TYPE ## MetaRegistration = qRegisterMetaType<TYPE>();

#define K_META_TYPE_ALIAS(TYPE, ALIAS) \
private: \
    static inline const int ALIAS ## MetaRegistration = qRegisterMetaType<TYPE>();

#if QT_VERSION < QT_VERSION_CHECK(5, 15, 0)
    #define K_QML_INTERFACE(TYPE) \
    private: \
        static inline const int TYPE ## QMLRegistration = qmlRegisterInterface<TYPE>(# TYPE);
#else
    #define K_QML_INTERFACE(TYPE) \
    private: \
        static inline const int TYPE ## QMLRegistration = qmlRegisterInterface<TYPE>(KLibInfo::libname, KLibInfo::major);
#endif


#define K_QML_SINGLETON(TYPE) \
private: \
    static QObject *qmlInstance(QQmlEngine *engine, QJSEngine *scriptEngine) { \
        (void)engine; \
        (void)scriptEngine; \
        return instance(); \
    } \
    static inline const int TYPE ## QMLRegistration = qmlRegisterSingletonType<TYPE>(KLibInfo::libname, KLibInfo::major, KLibInfo::minor, # TYPE, &TYPE::qmlInstance);

#define K_QML_SINGLETON_ALIAS(TYPE, ALIAS) \
private: \
    static QObject *qmlInstance(QQmlEngine *engine, QJSEngine *scriptEngine) { \
        (void)engine; \
        (void)scriptEngine; \
        return instance(); \
    } \
    static inline const int TYPE ## QMLRegistration = qmlRegisterSingletonType<TYPE>(KLibInfo::libname, KLibInfo::major, KLibInfo::minor, #ALIAS, &TYPE::qmlInstance);



template<typename T>
class KAutoPropertySaver {
    T *m_pointer;
    QString m_id;
public:
    KAutoPropertySaver(T *pointer, std::function<void(T)> setter, QString id) {
        m_pointer = pointer;
        m_id = id;
        QFile file(id);
        if(file.open(QIODevice::ReadOnly)) {
            auto ba = file.readAll();
            QDataStream stream(&ba, QIODevice::ReadOnly);
            T tmp;
            stream >> tmp;
            setter(tmp);
        }
    }
    ~KAutoPropertySaver() {
        QFile file(m_id);
        if(file.open(QIODevice::WriteOnly)) {
            QByteArray ba;
            QDataStream stream(&ba, QIODevice::WriteOnly);
            stream << *m_pointer;
            file.write(ba);
        }
    }
};

#define K_SAVED_PROPERTY(TYPE, NAME, GETTER, SETTER, NOTIFIER, DEFAULT) \
Q_PROPERTY(TYPE NAME READ GETTER WRITE SETTER NOTIFY NOTIFIER) \
    public: \
        TYPE GETTER() const { return this->m_ ## NAME; } \
        void SETTER(TYPE value) { \
            if (KCompareEngine<TYPE>::compare(this->m_ ## NAME, value)) return; \
            this->m_ ## NAME = value; \
            emit NOTIFIER(value); \
        } \
        Q_SIGNAL void NOTIFIER(TYPE value); \
    private: \
        TYPE m_ ## NAME = DEFAULT; \
        KAutoPropertySaver<TYPE> m_ ## NAME ## Saver = KAutoPropertySaver<TYPE>(&m_ ## NAME, [this](auto value){ SETTER(value); }, QString(typeid(this).name()) + ":" + #NAME);


#define K_READONLY_SAVED_PROPERTY(TYPE, NAME, GETTER, SETTER, NOTIFIER, DEFAULT) \
Q_PROPERTY(TYPE NAME READ GETTER NOTIFY NOTIFIER) \
public: \
    TYPE GETTER() const { return this->m_ ## NAME; } \
    Q_SIGNAL void NOTIFIER(TYPE value); \
private: \
    TYPE m_ ## NAME = DEFAULT; \
    void SETTER(TYPE value) { \
        if (KCompareEngine<TYPE>::compare(this->m_ ## NAME, value)) return; \
        this->m_ ## NAME = value; \
        emit NOTIFIER(value); \
    } \
    KAutoPropertySaver<TYPE> m_ ## NAME ## Saver = KAutoPropertySaver<TYPE>(&m_ ## NAME, [this](auto value){ SETTER(value); }, QString(typeid(this).name()) + ":" + #NAME);
