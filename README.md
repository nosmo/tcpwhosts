tcpwhosts
=======

tcpwhosts - a Python library for those who like their ACLs 1990s
style. It is a Pythonic interface to tcpwrappers hosts file (such as
/etc/hosts.deny or /etc/hosts.allow).

Usage
-------

tcpwhosts objects support basic object operations for adding,
removing, testing presence of addresses and so on.

This code:
```
tcpf = TCPWrapperHostsFile("/tmp/myfile")
tcpf += "10.0.0.2"
```

Results in ```/tmp/myfile``` containing:
```ALL: 10.0.0.2```

And the following:
```
tcpf = TCPWrapperHostsFile("/tmp/myfile")
tcpf += "10.0.0.2"
tcpf += "10.0.0.3"
```

Will result in ```/tmp/myfile``` being:
```ALL: 10.0.0.3```

All of the aforementioned operations (and some other ones) will
default to using ALL as the service.

To add records with specific services and to add comments, use the
```add``` function.

Requirements
-------
Nothing but stdlib.

Testing
-------
Some very simple tests can be run using ```tests.py```.

License
-------
N©!, 2014.
