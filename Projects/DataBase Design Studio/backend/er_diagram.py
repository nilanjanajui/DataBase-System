from graphviz import Digraph
import os

PROCESSED_FOLDER = os.path.join(os.getcwd(), "processed")


def generate_er_diagram_from_keymap(base_name: str, keymap: dict) -> bytes:
    dot = Digraph(comment="ER Diagram", format="png")
    dot.attr(rankdir="TB", splines="curved", nodesep="0.7", ranksep="0.7")
    dot.attr("graph", dpi="300")
    dot.attr("node", shape="plaintext", fontname="Helvetica", fontsize="12")

    table_border_color = "#4b555c"

    for table_name, key_info in keymap.items():
        attributes = key_info.get("attributes", [])
        primary_keys = set(key_info.get("primary_keys", []))
        foreign_keys = key_info.get("foreign_keys", {})

        # Build HTML-like label for the table node
        label = f"""<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="2" CELLPADDING="8" COLOR="{table_border_color}" STYLE="ROUNDED">
            <TR><TD BGCOLOR="{table_border_color}" ALIGN="CENTER">
                <FONT COLOR="white" POINT-SIZE="16"><B>{table_name}</B></FONT>
            </TD></TR>
        """

        for attr in attributes:
            if attr in primary_keys:
                attr_label = f"<B>{attr} (PK)</B>"
            elif attr in foreign_keys:
                attr_label = f"<I>{attr} (FK)</I>"
            else:
                attr_label = attr
            # Add attribute row with PORT named as attribute for edges
            label += f'<TR><TD PORT="{attr}" ALIGN="LEFT"><FONT POINT-SIZE="14">{attr_label}</FONT></TD></TR>'

        label += "</TABLE>>"
        dot.node(table_name, label=label)

    # Draw FK edges: from FK attribute port in current table
    # to PK attribute port in referenced table (better visualization)
    for table_name, key_info in keymap.items():
        foreign_keys = key_info.get("foreign_keys", {})

        for fk_attr, ref_info in foreign_keys.items():
            # FIX: ref_info is a dict with 'ref_table' and 'ref_column'
            ref_table = ref_info.get("ref_table")
            ref_column = ref_info.get("ref_column")

            if ref_table in keymap:
                pk_attrs = set(keymap[ref_table].get("primary_keys", []))
                # Use referenced column if it is a PK, else fallback to first PK
                target_port = (
                    ref_column
                    if ref_column in pk_attrs
                    else (list(pk_attrs)[0] if pk_attrs else "")
                )
                if target_port:
                    dot.edge(
                        f"{table_name}:{fk_attr}",
                        f"{ref_table}:{target_port}",
                        color=table_border_color,
                        fontsize="10",
                        arrowhead="normal",
                    )
                else:
                    # fallback edge without ports if no pk attribute found
                    dot.edge(
                        table_name, ref_table, color=table_border_color, fontsize="10"
                    )

    # Render to temporary file in PROCESSED_FOLDER
    temp_filepath = os.path.join(PROCESSED_FOLDER, f"{base_name}_temp")
    dot.render(filename=temp_filepath, cleanup=False)  # creates temp_filepath + ".png"

    png_path = temp_filepath + ".png"
    with open(png_path, "rb") as img_file:
        image_bytes = img_file.read()

    # Clean up temporary files
    for ext in [".png", ".gv"]:
        try:
            os.remove(temp_filepath + ext)
        except OSError:
            pass

    return image_bytes


from graphviz import Digraph
import os

PROCESSED_FOLDER = os.path.join(os.getcwd(), "processed")


def generate_er_diagram_from_keymap(base_name: str, keymap: dict) -> bytes:
    dot = Digraph(comment="ER Diagram", format="png")
    dot.attr(rankdir="TB", splines="curved", nodesep="0.3", ranksep="0.5")
    dot.attr("graph", dpi="300")
    dot.attr("node", shape="plaintext", fontname="Helvetica", fontsize="20")

    table_border_color = "#4b555c"

    for table_name, key_info in keymap.items():
        attributes = key_info.get("attributes", [])
        primary_keys = set(key_info.get("primary_keys", []))
        foreign_keys = key_info.get("foreign_keys", {})

        # Build HTML-like label for the table node with increased size
        label = f"""<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="10" CELLPADDING="18" COLOR="{table_border_color}" STYLE="ROUNDED">
            <TR>
                <TD BGCOLOR="{table_border_color}" ALIGN="CENTER" WIDTH="320" HEIGHT="20">
                    <FONT COLOR="white" POINT-SIZE="20"><B>{table_name}</B></FONT>
                </TD>
            </TR>
        """

        for attr in attributes:
            if attr in primary_keys:
                attr_label = f"<B>{attr} (PK)</B>"
            elif attr in foreign_keys:
                attr_label = f"<I>{attr} (FK)</I>"
            else:
                attr_label = attr
            # Add attribute row with PORT named as attribute for edges
            label += f'<TR><TD PORT="{attr}" ALIGN="LEFT"><FONT POINT-SIZE="14">{attr_label}</FONT></TD></TR>'

        label += "</TABLE>>"
        dot.node(table_name, label=label)

    # Draw FK edges: from FK attribute port in current table
    # to PK attribute port in referenced table
    for table_name, key_info in keymap.items():
        foreign_keys = key_info.get("foreign_keys", {})

        for fk_attr, ref_info in foreign_keys.items():
            ref_table = ref_info.get("ref_table")
            ref_column = ref_info.get("ref_column")

            if ref_table in keymap:
                pk_attrs = set(keymap[ref_table].get("primary_keys", []))
                target_port = (
                    ref_column
                    if ref_column in pk_attrs
                    else (list(pk_attrs)[0] if pk_attrs else "")
                )
                if target_port:
                    dot.edge(
                        f"{table_name}:{fk_attr}",
                        f"{ref_table}:{target_port}",
                        color=table_border_color,
                        fontsize="10",
                        arrowhead="normal",
                    )
                else:
                    dot.edge(
                        table_name, ref_table, color=table_border_color, fontsize="10"
                    )

    # Render to temporary file in PROCESSED_FOLDER
    temp_filepath = os.path.join(PROCESSED_FOLDER, f"{base_name}_temp")
    dot.render(filename=temp_filepath, cleanup=False)  # creates temp_filepath + ".png"

    png_path = temp_filepath + ".png"
    with open(png_path, "rb") as img_file:
        image_bytes = img_file.read()

    # Clean up temporary files
    for ext in [".png", ".gv"]:
        try:
            os.remove(temp_filepath + ext)
        except OSError:
            pass

    return image_bytes
