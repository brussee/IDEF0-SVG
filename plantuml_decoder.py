# Forked from https://gist.github.com/dyno/94ef6bb9644a88d6981d6a1a9eb70802
# https://plantuml.com/text-encoding
# https://github.com/dougn/python-plantuml/blob/master/plantuml.py#L64

import base64
import string
import zlib


plantuml_alphabet = (
    string.digits + string.ascii_uppercase + string.ascii_lowercase + "-_"
)
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
b64_to_plantuml = bytes.maketrans(
    base64_alphabet.encode("utf-8"), plantuml_alphabet.encode("utf-8")
)
plantuml_to_b64 = bytes.maketrans(
    plantuml_alphabet.encode("utf-8"), base64_alphabet.encode("utf-8")
)


def plantuml_encode(plantuml_text):
    """zlib compress the plantuml text and encode it for the plantuml server"""
    zlibbed_str = zlib.compress(plantuml_text.encode("utf-8"))
    compressed_string = zlibbed_str[2:-4]
    return (
        base64.b64encode(compressed_string).translate(b64_to_plantuml).decode("utf-8")
    )


def plantuml_decode(plantuml_url):
    """decode plantuml encoded url back to plantuml text"""
    data = base64.b64decode(plantuml_url.translate(plantuml_to_b64).encode("utf-8"))
    dec = zlib.decompressobj()  # without check the crc.
    header = b"x\x9c"
    return dec.decompress(header + data).decode("utf-8")


if __name__ == "__main__":
    url = "SyfFKj2rKt3CoKnELR1Io4ZDoSa700=="
    decoded = plantuml_decode(url)

    print(decoded)
    print(plantuml_encode(decoded))
    assert decoded == "Bob -> Alice : hello"

    print(
        plantuml_encode(
            """Cook Pizza receives Ingredients
Cook Pizza respects Customer Order
Cook Pizza respects Recipe
Cook Pizza requires Chef
Cook Pizza requires Kitchen
Cook Pizza produces Pizza
Take Order produces Customer Order
Take Order respects Menu
Take Order requires Wait Staff
Eat Pizza receives Pizza
Eat Pizza receives Hungry Customer
Eat Pizza produces Satisfied Customer
Eat Pizza produces Mess
"""
        )
    )
