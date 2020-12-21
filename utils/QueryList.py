from __future__ import annotations


class QueryList:
    def __init__(self, list=[]):
        self.__list__ = list

    def Select(self, selectorfunc):
        return QueryList([selectorfunc(x) for x in self.__list__])

    def SelectMany(self, collectionselector):
        l = []
        for x in collectionselector(self.__list__):
            l.append(x)
        return QueryList(l)

    def Where(self, condition):
        l = []
        for x in self.__list__:
            if condition(x):
                l.append(x)
        return QueryList(l)

    def OfType(self, t):
        return self.Where(lambda x: isinstance(x, t))

    def OrderBy(self, keyselector):
        self.__list__.sort(key=keyselector)
        return QueryList(self.__list__)

    def Reverse(self):
        return QueryList(self.__list__[::-1])

    def GroupBy(self, keyselector):
        keys = self.Select(keyselector)
        l = []
        for key in keys:
            val = self.Where(lambda x: keyselector(x) == key)
            keydict = {"key": key, "group": val}
            l.append(keydict)

        return QueryList(l)

    def All(self, condition):
        for x in self.__list__:
            if not condition(x):
                return False
        return True

    def Any(self, condition):
        for x in self.__list__:
            if condition(x):
                return True
        return False

    def Contains(self, element, comparatorfunc=None):
        if comparatorfunc == None:
            return element in self.__list__
        else:
            for x in self.__list__:
                if comparatorfunc(element, x):
                    return True
            return False

    def Aggregate(self, aggregationfunction, seeder=None):
        if seeder == None:
            aggregate = aggregationfunction(self.__list__[0], self.__list__[1])
            for x in self.__list__[2:]:
                aggregate = aggregationfunction(aggregate, x)
            return aggregate
        else:
            aggregate = aggregationfunction(seeder, self.__list__[0])
            for x in self.__list__[1:]:
                aggregate = aggregationfunction(aggregate, x)
            return aggregate

    def Average(self, keyselector=lambda x: x):
        if (len(self.__list__)) == 0:
            return 0
        return self.Aggregate(lambda x, y: x + y) / len(self.__list__)

    def Count(self, condition=lambda x: True):
        return len(self.Where(condition))

    def Max(self, keyselector=lambda x: x):
        return max(self.__list__, key=keyselector)

    def Min(self, keyselector=lambda x: x):
        return min(self.__list__, key=keyselector)

    def Sum(self, keyselector=lambda x: x):
        return self.Average(keyselector) * self.Count()

    def ElementAt(self, index):
        return self.__list__[index]

    def ElementAtOrDefault(self, index, default):
        if index >= self.Count() or index < 0:
            return default
        else:
            return self.ElementAt(index)

    def First(self, condition=lambda x: True):
        return self.Where(condition).ElementAt(0)

    def FirstOrDefault(self, default, condition=lambda x: True):
        return self.Where(condition).ElementAtOrDefault(0, default)

    def Last(self, condition=lambda x: True):
        return self.Where(condition).ElementAt(self.Count() - 1)

    def Last(self, default, condition=lambda x: True):
        return self.Where(condition).ElementAtOrDefault(self.Count() - 1, default)

    def Single(self, condition):
        l = self.Where(condition)
        if l.Count() != 1:
            raise KeyError()
        return l.ElementAt(0)

    def SingleOrDefault(self, condition, default):
        l = self.Where(condition)
        if l.Count() != 1:
            return default
        return l.ElementAt(0)

    def SequenceEqual(self, other: QueryList, comparator=lambda x, y: x == y):
        if self.Count() != other.Count():
            return False

        for i in range(0, self.Count()):
            if not comparator(self.ElementAt(i), other.ElementAt(i)):
                return False

        return True

    def Concat(self, other: QueryList):
        return QueryList(self.__list__ + other.__list__)

    def Distinct(self):
        l = []
        for x in self.__list__:
            if x not in l:
                l.append(x)
        return QueryList(l)

    def Except(self, other: QueryList):
        l = []
        for x in self.__list__:
            if x not in other:
                l.append(x)
        return QueryList(l)

    def Intersect(self, other: QueryList):
        l = []
        for x in self.__list__:
            if x in other:
                l.append(x)
        return QueryList(l)

    def Union(self, other: QueryList):
        return self.Concat(other).Distinct()

    def Skip(self, num):
        return QueryList(self.__list__[num:])

    def Take(self, num):
        return QueryList(self.__list__[:num])

    def Cast(self, t: type):
        return self.Select(lambda x: t.__init__(x))

    def ToList(self):
        return self.__list__

    def Add(self, element):
        self.__list__.append(element)

    def AddRange(self, elements):
        return self.Concat(elements)

    def Clear(self):
        self.__list__ = []

    def Find(self, condition):
        return self.First(condition)

    def ForEach(self, foreach):
        for x in self.__list__:
            foreach(x)

    def Insert(self, index, element):
        self.__list__.insert(index, element)

    def InsertRange(self, index, elements):
        return QueryList(self.__list__[:index] + elements + self.__list__[index:])

    def Remove(self, element):
        self.__list__.remove(element)

    def RemoveAt(self, index):
        self.__list__.pop(index)

    def RemoveRange(self, condition):
        l = []
        for x in self.__list__:
            if not condition(x):
                l.append(x)
        return QueryList(l)

    def Sort(self):
        self.__list__.sort()

    def __getitem__(self, index):
        return self.__list__[index]
