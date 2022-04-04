## Path Manager
The PathManager class in path.py is used for adding paths and loading classes from those paths

The add_path method takes the intended name of the class, the type of the class (either data, model or feature extractor) and the path to the target python file

Once the path has been added the class can be instantiated with the load method from the path manager.  The load functions takes the name and type of class as arguments.

The user uploaded python files must implement the abstract classes for either data, feature extractors or models.  There are examples in the data and models folders.

The path manager stores its state in the path_dict.pkl file



## Result Manager

Used to quickly load previous prediction arrays

Result objects are uploaded with the add_result method.  They are stored in redis for later.

Results can be loaded with the load_result method which returns the array that was previously stored.

When a result is uploaded the a hash of the file at the target path is also stored.  When the result is loaded later the current hash of the target file is compared to the old hash to check if the file has been modified.