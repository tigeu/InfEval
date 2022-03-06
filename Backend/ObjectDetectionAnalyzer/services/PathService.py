import os
import shutil
from pathlib import Path


class PathService:
    """
    Service that contains method for several path actions like creating directories, or combining them.

    Methods
    -------
    get_combined_dir(path, name)
        Combines a path and file name together into a new path

    create_dir(dir, recreate=False)
        Create given directory. If recreate, delete old directory and create new one

    get_dataset_dir(user_dir, dataset_name)
        Get dataset directory for a given user directory and a given dataset name

    get_prediction_dir(dataset_dir)
        Get prediction directory for a given dataset directory

    get_model_dir(user_dir, model_name)
        Get model directory for a given user directory

    save_tmp_file(tmp_dir, file_name, file_obj)
        Save uploaded file_obj temporarily in tmp_dir under given file_name

    delete_tmp_file(tmp_file_path)
        Delete temporarily saved file

    delete(object)
        Deletes a given object, whether file or directory. Useful for updating models (TF is a folder, YOLO a file)

    get_filed_from_dir(dir)
        Gets all files from a given directory

    get_image_files_from_dir(dir, image_endings)
        Gets all image files from a given directory that have an ending in image_endings
    """

    def get_combined_dir(self, path, name):
        """
        Combines a path and file name together into a new path.

        Parameters
        ----------
        path : Path
            Path of the directory
        name : str
            File name

        Returns
        -------
        Path
            Path of file in given path. None if path or name not given.
        """
        if path and name:
            return Path(path / name)

    def create_dir(self, dir, recreate=False):
        """
        Create given directory. If recreate, delete old directory and create new one

        Parameters
        ----------
        path : Path
            Path of the directory
        recreate : bool
            Indicates whether an existing directory should be recreated

        Returns
        -------
        bool
            Indicates if directory was successfully created
        """
        if recreate and dir.is_dir():
            shutil.rmtree(dir)

        if dir:
            Path(dir).mkdir(parents=True, exist_ok=True)
            return True

        return False

    def get_dataset_dir(self, user_dir, dataset_name):
        """
        Get dataset directory for a given user directory and a given dataset name

        Parameters
        ----------
        user_dir : Path
            Directory of current user
        dataset_name : str
            Name of current dataset

        Returns
        -------
        Path
            Path of the current dataset. None if user_dir or dataset_name not given
        """
        if user_dir and dataset_name:
            dataset_dir = user_dir / "datasets" / dataset_name
            return Path(dataset_dir)

    def get_predictions_dir(self, dataset_dir):
        """
        Get prediction directory for a given dataset directory

        Parameters
        ----------
        dataset_dir : Path
            Path of current dataset

        Returns
        -------
        Path
            Path of the prediction_dir for current dataset. None if dataset_dir not given
        """
        if dataset_dir:
            predictions_dir = dataset_dir / "predictions"
            return Path(predictions_dir)

    def get_model_dir(self, user_dir, model_name):
        """
        Get model directory for a given user directory

        Parameters
        ----------
        user_dir : Path
            Directory of current user
        model_name : str
            Name of current model

        Returns
        -------
        Path
            Path of the model directory for current user. None if user_dir or model_name not given
        """
        if user_dir and model_name:
            model_dir = user_dir / "models" / model_name
            return Path(model_dir)

    def save_tmp_file(self, tmp_dir, file_name, file_obj):
        """
        Save uploaded file_obj temporarily in tmp_dir under given file_name

        Parameters
        ----------
        tmp_dir : Path
            Directory of temporary files
        file_name : str
            Name of current file
        file_obj : file
            Current file object

        Returns
        -------
        Path
            Path of temporarily saved file
        """
        if self.create_dir(tmp_dir) and file_name and file_obj:
            tmp_file_path = self.get_combined_dir(tmp_dir, file_name)
            with open(tmp_file_path, "wb") as file:
                file.write(file_obj.read())
            return tmp_file_path

    def delete_tmp_file(self, tmp_file_path):
        """
        Delete temporarily saved file

        Parameters
        ----------
        tmp_file_path : Path
            Path of temporarily saved file
        """
        Path.unlink(tmp_file_path)

    def delete(self, object):
        """
        Deletes a given object, whether file or directory. Useful for updating models (TF is a folder, YOLO a file)

        Parameters
        ----------
        object : any
            File or Directory
        """
        if object.is_dir():
            shutil.rmtree(object)
        else:
            Path.unlink(object)

    def get_files_from_dir(self, dir):
        """
        Gets all files from a given directory

        Parameters
        ----------
        dir : Path
            Directory from which all files should be retrieved

        Returns
        -------
        List
            List of all image names in the given directory
        """
        return os.listdir(dir)

    def get_image_files_from_dir(self, dir, image_endings):
        """
        Gets all image files from a given directory that have an ending in image_endings

        Parameters
        ----------
        dir : Path
            Directory from which all files should be retrieved
        image_endings : list
            List of wanted file endings for images

        Returns
        -------
        List
            List of image names that have the expected file endings
        """
        image_names = []
        for file_name in os.listdir(dir):
            extension = os.path.splitext(file_name)[1]
            if extension.lower() in image_endings:
                image_names.append(os.path.join(dir, file_name))

        return image_names
