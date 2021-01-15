#include "loginservice.h"
#include <QCryptographicHash>
#include <QDateTime>
#include <QDebug>

LoginService::LoginService(QObject *parent) : QObject(parent)
{
    this->dProvider = new SqliteProvider("../../ServerClientQML/QML.db");
}

bool LoginService::login(QString username, QString pass)
{
    dProvider->setTable("User");
    QVariant result = dProvider->getRowField("username", username);
    if(!result.isValid()) return false;
//    QString usernameFromDB = result.toString();
    QString hashedPass = QCryptographicHash::hash(pass.toUtf8(), QCryptographicHash::Sha256);
    if(dProvider->getRowField("password", hashedPass).isValid()) {
        m_user.name = result.toString();
        m_user.uid = dProvider->getRowField("username", username, 0).toInt();
        createSession();
        return true;
    }
    return false;
}

bool LoginService::logout()
{
    if(logged) {
        logged = !logged;
        return true;
    }
    else return logged;
}

bool LoginService::signup(QString newUserName, QString pass)
{
    dProvider->setTable("User");
    QString hashedPass = QCryptographicHash::hash(pass.toUtf8(), QCryptographicHash::Sha256);
    if(dProvider->getRowField("username", newUserName).toString() != newUserName) {
        qDebug() << dProvider->getRowField("username", newUserName).toString();
        m_user.name = newUserName;
        m_user.uid = dProvider->getRowField("username", newUserName, 0).toInt();
        createSession();
        return dProvider->insertRow({{"username", newUserName}, {"password", hashedPass}});
    }
    qDebug() << "User already exists";
    return false;
}

bool LoginService::changePassWord(QString user, QString oldPassword, QString newPassword)
{
    dProvider->setTable("User");
    QString hashedOldPassword = QCryptographicHash::hash(oldPassword.toUtf8(), QCryptographicHash::Sha256);
    QVariant result = dProvider->getRowField("username", user);
    if(result.isValid()) {
        QString pass = result.toString();
        if(pass == hashedOldPassword) {
            return dProvider->updateRow({{"password", newPassword}}, {"id", dProvider->getRowField("username", user).toInt()});
        }
        else return false;
    }
    return false;
}

bool LoginService::createSession()
{
    dProvider->setTable("Session");
    if(!dProvider->insertRow({{"userID", m_user.uid}, {"date", QDateTime::currentDateTime().toString(Qt::ISODate)}})) return false;
    sessionID = dProvider->getLastID();
    if(sessionID == -1) return false;
    return true;
}

User LoginService::user()
{
    return m_user;
    //QVariant result = dProvider->getRow()
//    User user {
//      ->username = ;
//    };
}
