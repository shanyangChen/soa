SOA
===

Overview
--------
- To build up a python server by simple (for fun).
- Base on python3.6+ and asynicio.
- Build up by pure python language first and update by cython to
  optimize the asynic funcs for network.

Feature highlights
------------------
- It is a learning work for web and other framework, so fork it and up with us.
- The version 0.0.1- means that It is not a complete framework, but I hope you
  will like it gradually.

Version
-------
- 0.0.1-

Setup
-----
(Should I make a makefile?(^ .~))
``git clone https://github.com/wangsong19/soa``
.. code:: shell
    cd soa
    python3 setup.py sdist
    
    cd soa/dist/
    tar xvzf SOA0.0.1-.tar.gz

    cd SOA0.0.1-
    python3 setup.py install

    rm -rf /dist

Simple test
-----------
.. code:: python
    
    def hello(request):
        # set headers example
        request.set_headers({'Content-Type':'text/css; charset=utf-8'})
        
        return 'hello SOA !'

