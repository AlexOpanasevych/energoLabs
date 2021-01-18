#ifndef DATAPROVIDER_H
#define DATAPROVIDER_H

#include <QObject>
#include "kmacro.h"
#include <sqliteprovider.h>
#include "kobservablelist.h"


class DataProvider : public QObject
{
    Q_OBJECT
    K_QML_TYPE(DataProvider)
    SqliteProvider p;



public:
    explicit DataProvider(QObject *parent = nullptr);

public slots:
    QVariantList thirdGraphData(int dayFirst, int daySecond);
    QList<QVariantMap> userGraphConsume(int userId);

signals:



};

#endif // DATAPROVIDER_H
