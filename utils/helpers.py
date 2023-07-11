def build_url_with_params(url: str, params: dict) -> str:
    """
    Builds a URL with the given parameters.

    Args:
        url (str): The URL to build.
        params (dict): The parameters to add to the URL.

    Returns:
        str: The built URL.
    """

    # if url includes ? only add the parameters with & between them

    if "?" in url:
        return url + "&" + "&".join([f"{key}={value}" for key, v in params.items() for value in v])

    return url + "?" + "&".join([f"{key}={value}" for key, v in params.items() for value in v])
