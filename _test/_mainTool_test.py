from Style import Style
from mods.mainTool import MainTool, FileHandler, App
import Style as St

def test_main_tool():
    # Create an instance of the MainTool class
    main_tool = MainTool(v="1.0.0", tool={}, name="TestTool", logs=[], color="RED", on_exit=None, load=None)

    # Initialize the tool by calling the load method

    # Verify that the print method works as expected
    main_tool.print("Hello, world!")

    assert main_tool.logs == [[main_tool, "no load require"], [main_tool, "TOOL successfully loaded"]]


def get_app():
    return App("test-")


def app_clean_up(app):
    app.exit_all_modules()
    app.exit()


def test_main():
    # Create an instance of the MainTool class

    app = get_app()

    f = app.load_all_mods_in_file('../mods/')

    assert f == app.alive
    app_clean_up(app)


def test_FileHandler():
    # Create a FileHandler object with a sample filename
    fh = FileHandler("sample.config")

    # Verify that the object was initialized correctly
    assert fh.file_handler_filename == "sample.config"
    assert fh.file_handler_index_ == -1
    assert fh.file_handler_file_prefix == ".config/mainTool/"

    # Open the storage file in write mode and verify that it was opened correctly
    fh.open_s_file_handler()
    assert fh.file_handler_storage is not None

    # Add some data to the save file and verify that it was added correctly
    key, value = "key1~~~~~:", "value1"
    fh.add_to_save_file_handler(key, value)
    fh.add_to_save_file_handler("key2~~~~~:", "value2")
    fh.add_to_save_file_handler("key3~~:", "value3")
    assert fh.file_handler_save == ["key1~~~~~:value1", "key2~~~~~:value2"]

    # Save the data to the storage file and verify that it was saved correctly
    fh.save_file_handler()

    # Open the storage file in read mode and verify that it was opened correctly

    fh.open_l_file_handler()
    fh.load_file_handler()

    assert fh.file_handler_load[0][0] == key
    assert fh.file_handler_load[0][1] == value


if __name__ == '__main__':
    s = St.Style()
    print(s.Underline + "test_main_tool Test " + Style.BEIGEBG("started"))
    test_main_tool()

    print(s.Underline+"app_clean_up Test " +Style.BEIGEBG("started"))
    app_clean_up(get_app())

    print(s.Underline+"test_main Test " +Style.BEIGEBG("started"))
    test_main()

    print(s.Underline+"test_FileHandler Test " +Style.BEIGEBG("started"))
    test_FileHandler()

    print(s.GREEN("MainTool Tests " +Style.BLINK("successfully")))
