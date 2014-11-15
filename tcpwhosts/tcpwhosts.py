#!/usr/bin/env python

"""Somewhat pythonic interface to the tcpwrappers hosts.deny and
hosts.allow format.

  HostsFile is a generic class for hosts files with an arbitrary
 location. HostsDeny and HostsAllow simply point to the standard
 locations.

"""

__author__ = "nosmo@nosmo.me"


class TCPWrapperHostsFile(object):
    """Interface to tcpwrappers hosts.* files"""

    def __init__(self, path, buffer_writes=0):
        """Access a hosts file

        Arguments:
         path -- string path to the hosts file to use.
        Keyword arguments:
         buffer_writes -- the number of writes to buffer for writing.
        """

        self.filepath = path
        self.hosts_data = None
        self.buffer_writes = buffer_writes

        if buffer_writes:
            self.buffer = []
        else:
            self.buffer = None

    def __load_data(self):
        """Load data from the hosts file"""
        linedata = []
        with open(self.filepath, "r") as fileobj:
            for line in fileobj.read().split("\n"):
                if line.startswith("#"):
                    continue

                linesplit = line.split()
                if len(linesplit) == 2:
                    # No comment
                    linesplit.append(None)
                if linesplit:
                    linedata.append(linesplit)
        return linedata

    @staticmethod
    def __render_entry(linesplit):
        """Render a tuple representing a hostsfile entry"""
        commentstr = ""

        if linesplit[2] and not linesplit[2].startswith("#"):
            commentstr = "#%s" % linesplit[2]
        elif linesplit[2]:
            commenstr = linesplit[2]

        return "%s %s %s" % (
            linesplit[0],
            linesplit[1],
            commentstr
            )

    def add(self, ipaddress, bantype="ALL", comment=None):
        """Add to a hosts file.

        Arguments:
         ipaddress -- ip address tring
        Keyword arguments:
         bantype -- the service used to classify the ban. Defaults to ALL.
         comment -- the comment to append with a #
        """

        self.hosts_data = self.__load_data()
        bantype = "%s:" % bantype
        lineentry = self.__render_entry([bantype, ipaddress, comment])

        # if entry is the same, do nothing
        if [bantype, ipaddress, comment] in self.hosts_data:
            return self

        # if entry exists, update/replace.
        for index, entry in enumerate(self.hosts_data):
            if entry[1] == ipaddress:
                self.hosts_data[index][0] = bantype
                self.hosts_data[index][2] = comment
                return self

        if self.buffer_writes:
            self.buffer.append(lineentry)

        # finally, just add it
        if not self.buffer_writes:
            with open(self.filepath, "a") as fileobj:
                fileobj.write(
                    "%s\n" % lineentry
                    )
        elif self.buffer_writes and len(self.buffer) >= self.buffer_writes:
            print "Paging out writes"
            for entry in self.buffer:
                with open(self.filepath, "a") as fileobj:
                    fileobj.write(
                        "%s\n" % entry
                        )

        self.hosts_data += [bantype, ipaddress, comment]

        # TODO: return something better
        return self

    def __add__(self, ipaddress):
        """Add an IP address to the hosts file using ALL: as the type.

        Arguments:
         ipaddress -- the ipaddress to add.
        """
        self.hosts_data = self.__load_data()
        comment = None
        bantype = "%s:" % "ALL"
        lineentry = self.__render_entry([bantype, ipaddress, comment])

        # finally, just add it
        with open(self.filepath, "a") as fileobj:
            fileobj.write(
                "%s\n" % lineentry
            )
        self.hosts_data = [bantype, ipaddress, comment]

        # TODO: return something better
        return self

    def __sub__(self, ipaddress):
        """Remove an IP address from the hosts file

        Arguments:
         ipaddress -- the IP address to remove.
        """

        out_data = []
        self.hosts_data = self.__load_data()
        for line in self.hosts_data:
            if line[1] != ipaddress:
                out_data.append(line)

        with open(self.filepath, "w") as fileobj:
            for out_line in out_data:
                fileobj.write("%s\n" % self.__render_entry(out_line))

        self.hosts_data = out_data
        # TODO: return something better
        return self

    def __contains__(self, ipaddress):
        """Check whether an IP address is in the hosts file.

        Arguments:
         ipaddress -- the IP address to look for
        """

        self.hosts_data = self.__load_data()
        for line in self.hosts_data:
            if len(line) > 1 and line[1] == ipaddress:
                return True
        return False

    def __len__(self):
        """Return the length of the hosts file. """
        num_lines = 0
        self.hosts_data = self.__load_data()
        for line in self.hosts_data:
            if not line[0].startswith("#"):
                num_lines += 1
        return num_lines

    def __iter__(self):
        """Iterate over the entries in the hosts file"""
        self.hosts_data = self.__load_data()
        for line in self.hosts_data:
            yield line

    def __nonzero__(self):
        """Is the hostsfile populated"""
        if self.__len__() > 0:
            return True
        else:
            return False

    # TODO __setitem__
    def __getitem__(self, ipaddress):
        """Return the entry for a particular IP address"""
        self.hosts_data = self.__load_data()
        for line in self.hosts_data:
            if len(line) > 1 and line[1] == ipaddress:
                return line
        return None

    def __bool__(self):
        return self.__nonzero__()

class HostsDeny(TCPWrapperHostsFile):
    """tcpwhosts interface for /etc/hosts.deny"""

    def __init__(self, buffer_writes=0):
        """Create a hosts file object for hosts.deny"""
        TCPWrapperHostsFile.__init__(self, "/etc/hosts.deny",
                                     buffer_writes=buffer_writes)

class HostsAllow(TCPWrapperHostsFile):
    """tcpwhosts interface for /etc/hosts.allow"""

    def __init__(self, buffer_writes=0):
        """Create a hosts file object for hosts.allow"""
        TCPWrapperHostsFile.__init__(self, "/etc/hosts.allow",
                                     buffer_writes=buffer_writes)
