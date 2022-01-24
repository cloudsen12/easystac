import errno
import json
import os
from pathlib import Path

import six
from termcolor import colored

STAC_SERVERS = {
    "pc": "Planetary Computer",
    "radiant": "Radiant MLHub",
}
CREDENTIAL_PATH = "~/.config/easystac/"

def get_credentials_path(stac_server: str = "radiant"):
    """Returns the path to the credentials file"""
    path_name = "%s/credentials_%s.json" % (CREDENTIAL_PATH, stac_server)
    return Path(path_name).expanduser()


def write_token(refresh_token: str, stac_server: str = "radiant"):
    """Attempts to write the passed token to the given user directory"""
    credentials_path = get_credentials_path(stac_server=stac_server)
    dirname = credentials_path.parent
    try:
        dirname.mkdir()
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise Exception("Error creating directory %s: %s" % (dirname, e))

    file_content = json.dumps({"token": refresh_token})
    # Remove file because os.open will not change permissions of existing files
    if credentials_path.exists():
        credentials_path.unlink()
    with os.fdopen(
        os.open(credentials_path, os.O_WRONLY | os.O_CREAT, 0o600), "w"
    ) as f:
        f.write(file_content)
    return True


def get_authorization_url(stac_server="pc"):
    if stac_server == "pc":
        return "https://mlhub.earth/profile" # TODO CHANGE BY PLANETARY
    elif stac_server == "radiant":
        return "https://mlhub.earth/profile"


def obtain_and_write_token(token=None, stac_server: str = "radiant"):
    """Obtains and writes credentials token based on an authorization code."""
    if token is None:
        display_auth_instructions(stac_server)
        token = input("Enter token: ")

    if isinstance(token, six.string_types):
        write_token(token, stac_server)
        print("\nSuccessfully saved authorization token.")
    else:
        raise Exception("Invalid token type: %s" % type(token))


# Display instructions for obtaining an authorization token ---------
def display_auth_instructions(stac_server="radiant"):
    ss_name = colored(STAC_SERVERS[stac_server], attrs=["bold"])
    if stac_server == "radiant":
        main_message = "To authorize access needed by %s, %s" % (
            ss_name,
            display_auth_instructions_radiant(),
        )
        print(main_message)
    elif stac_server == "pc":
        main_message = "To authorize access needed by %s, %s" % (
            ss_name,
            display_auth_instructions_radiant(),
        )
        print(main_message)
    return False


def display_auth_instructions_planetary():
    radiant_url = "https://mlhub.earth/profile"
    return (
        "open the following URL: %s in your web browser. "
        % colored(radiant_url, attrs=["bold"])
        + "An API key is required to access the Radiant MLHub API "
        + ", so please copy and paste it below."
    )


def display_auth_instructions_radiant():
    radiant_url = "https://mlhub.earth/profile"
    return (
        "open the following URL: %s in your web browser. "
        % colored(radiant_url, attrs=["bold"])
        + "An API key is required to access the Radiant MLHub API "
        + ", so please copy and paste it below."
    )
