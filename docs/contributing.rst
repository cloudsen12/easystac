Contributing
============

Contributions to easystac are welcome! Here you will find how to do it:

- **Bugs:** If you find a bug, please report it by opening an issue. if possible, please attach the error, code, version, and other details. 

- **Fixing Issues:** If you want to contributte by fixing an issue, please check the easystac issues: contributions are welcome for open issues with labels :code:`bug` and :code:`help wanted`.

- **Enhancement:** New features and modules are welcome! You can check the easystac issues: contributions are welcome for open issues with labels :code:`enhancement` and :code:`help wanted`.

- **Documentation:** You can add examples, notes and references to the easystac documentation by using the NumPy Docstrings of the easystac documentation, or by creating blogs, tutorials or papers.

First, fork the `easystac <https://github.com/cloudsen12/easystac>`_ repository and clone it to your local machine. Then, create a development branch::

   git checkout -b name-of-dev-branch
   
Create a new method, or fix a bug:

.. code-block:: python
   
   def my_new_method(x,other):
        '''Returns the addition of and image and a float.
    
        Parameters
        ----------    
        x : float
            Float to add.
        other : float
            Float to add.

        Returns
        -------    
        float
            Addition of two floats.

        Examples
        --------
        >>> import easystac as es
        >>> es.my_new_method(0.5,0.5)
        1.0
        '''
        return x + other

Remember to use `Black <https://github.com/psf/black>`_ and `isort <https://pycqa.github.io/isort/>`_!

In order to test additions, you can use :code:`pytest` over the :code:`tests` folder::

   pytest tests
   
If you have added a new feature, please include it in the tests.

To test across different Python versions, please use :code:`tox`.

Now it's time to commit your changes and push your development branch::

   git add .
   git commit -m "Description of your work"
   git push origin name-of-dev-branch
  
And finally, submit a pull request.