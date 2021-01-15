#ifndef LOGINSERVICE_H
#define LOGINSERVICE_H

#include <QObject>
#include <QString>
#include "sqliteprovider.h"

struct DATABASE_EXPORT User {
    QString name;
    int uid;
};

struct DATABASE_EXPORT Session {
    User user;
    int sessionId;
};

class DATABASE_EXPORT LoginService : public QObject
{
    Q_OBJECT
public:
    explicit LoginService(QObject *parent = nullptr);

    Q_INVOKABLE bool login(QString username, QString pass);
    Q_INVOKABLE bool logout();
    Q_INVOKABLE bool signup(QString newUserName, QString pass);
    Q_INVOKABLE bool changePassWord(QString user, QString oldPassword, QString newPassword);
    bool createSession();
    User user();
    int sessionID;
    int userID;

signals:

private:
    SqliteProvider * dProvider = nullptr;
    bool logged = false;
    User m_user;
};

#endif // LOGINSERVICE_H
