#ifndef OBSERVABLELIST_H
#define OBSERVABLELIST_H

#include <QObject>
#include <QAbstractItemModel>
#include <QRegularExpression>
#include <QHash>
#include <QByteArray>
class KObservableModel;

template <class T>
class KObservableList {
public:
    explicit KObservableList();
    ~KObservableList();
    void push_back(T*);
    void push_front(T*);
    T* get(int);
    T* first();
    T* last();
    void remove(int);
    void remove(T*);
    T* takeAt(int ind);
    inline int indexOf(T*);
    void clear();
    void insert(int, T*);
    int count(){return m_data.count();}
    auto begin() const { return m_data.begin(); }
    auto end() const { return m_data.end(); }
    void setFilterRule(const QString &property, const QRegularExpression &regex);

    KObservableModel* model() { return m_modelShell; }

private:
//    std::function<>
    QList<T*> m_data;
    KObservableModel *m_modelShell;
    QPair<QString, QRegularExpression> m_filterRule;
    bool filt(QVariant value);
};
class KObservableModel : public QAbstractListModel
{
    Q_OBJECT
    template<typename> friend class KObservableList;
public:
    //ObservableModel(){}
    int rowCount(const QModelIndex &) const override {
        return m_sizzer();
    }
    QVariant data(const QModelIndex &index, int) const override {
        auto object = m_getter(index.row());
        if(m_filter(object)) {
            return QVariant::fromValue(object);
        }

        return QVariant::fromValue<QObject*>(nullptr);
    }
//static_cast<int>(Qt::UserRole) + 1
//    QByteArray("object", 6)
//    QHash<int, QByteArray> roleNames() const override { return QHash<int, QByteArray>().insert(1, QByteArray());}

public slots:
    void updateModel() { emit modelReset({}); }
    int count() { return m_sizzer(); }
private:
    std::function<QObject*(int)> m_getter;
    std::function<int()> m_sizzer;
    std::function<bool(QObject*)> m_filter;
};


template<class T>
KObservableList<T>::KObservableList() {
    m_modelShell = new KObservableModel();
    m_modelShell->m_getter = [this](int ind){ return static_cast<QObject*>(this->m_data[ind]); };
    m_modelShell->m_sizzer = [this](){ return this->m_data.count(); };
    m_modelShell->m_filter = [this](QObject* object) { return m_filterRule.first.isEmpty() ? true : filt(object->property(m_filterRule.first.toStdString().c_str())); };
}

template<class T>
KObservableList<T>::~KObservableList() {
    delete m_modelShell;
}

template<class T>
void KObservableList<T>::push_front(T *v)
{
    m_modelShell->beginInsertRows(QModelIndex(), 0, 0);
    m_data.push_front(v);
    m_modelShell->endInsertRows();
}

template<class T>
void KObservableList<T>::push_back(T *v)
{
    m_modelShell->beginInsertRows(QModelIndex(), m_data.count(), m_data.count());
    m_data.append(v);
    m_modelShell->endInsertRows();
}

template<class T>
T* KObservableList<T>::first()
{
    return m_data.first();
}

template<class T>
T* KObservableList<T>::last()
{
    return m_data.last();
}

template<class T>
T *KObservableList<T>::get(int ind)
{
    return m_data[ind];
}

template<class T>
void KObservableList<T>::remove(int ind)
{
    m_modelShell->beginRemoveRows(QModelIndex(), ind, ind);
    auto r =  m_data.takeAt(ind);
    Q_UNUSED(r)
    m_modelShell->endRemoveRows();
}

template<class T>
T* KObservableList<T>::takeAt(int ind)
{
    m_modelShell->beginRemoveRows(QModelIndex(), ind, ind);
    auto r =  m_data.takeAt(ind);
    m_modelShell->endRemoveRows();
    return r;
}

template<class T>
void KObservableList<T>::remove(T *v)
{
    int ind = m_data.indexOf(v);
    m_modelShell->beginRemoveRows(QModelIndex(), ind, ind);
    m_data.removeAt(ind);
    m_modelShell->endRemoveRows();

}

template<class T>
int KObservableList<T>::indexOf(T *v)
{
    return m_data.indexOf(v);
}

template<class T>
void KObservableList<T>::clear()
{
    m_modelShell->beginResetModel();
    m_data.clear();
    m_modelShell->endResetModel();
}

template<class T>
void KObservableList<T>::insert(int pos, T *v)
{
    if (pos > m_data.size() - 1) push_back(v);
    else if (pos < 0){

        m_modelShell->beginInsertRows(QModelIndex(), 0, 0);
        m_data.push_front(v);
        m_modelShell->endInsertRows();
    }
    else
    {
        m_modelShell->beginInsertRows(QModelIndex(), pos, pos);
        m_data.insert(pos, v);
        m_modelShell->endInsertRows();
    }
}

template<class T>
void KObservableList<T>::setFilterRule(const QString &property, const QRegularExpression &regex) {
    m_filterRule = { property, regex };
    m_modelShell->dataChanged(m_modelShell->index(0), m_modelShell->index(m_modelShell->m_sizzer()));
}

template<class T>
bool KObservableList<T>::filt(QVariant value) {
    if(value.isNull())
        return false;

    QRegularExpressionMatch match = m_filterRule.second.match(value.toString());
    return match.capturedTexts().size() > 0;
}


#endif // OBSERVABLELIST_H
