# PyTUF


### Steps to run

0. Write Python classes for data, feature extractors or classifiers that implement our abstract class (see examples in the test folder)
    * Files should import from the app.abstract folder for example an import for a data class might look like: 

        `from app.abstract.data import Data`
    * The application is **built to work with numpy matrices** so data, feature extractors and classifiers should all output numpy matrices
1. Install required packages:
    * numpy
    * pickleDB
    * sklearn
    * matplotlib
    * EEL
2. Run gui.py
3. Upload your code using the upload button for the target category
4. Select an entry for data, feature extractor and classifier
5. Click the run button
    * You can optionally check the cache results button to save the result for retrieval at any time during the session
6. View the matplotlib diagram for scoring results
    * The diagram must be closed before another can be generated
