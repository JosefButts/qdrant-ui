from typing import Any, Dict, List

import streamlit as st


def create_filter_condition(
    filter_type: str, key: str, operator: str, value: Any
) -> Dict:
    """Create a filter condition based on the operator type."""
    if operator == "match":
        return {"key": key, "match": {"value": value}}
    elif operator == "range":
        return {"key": key, "range": value}
    elif operator == "geo_radius":
        return {"key": key, "geo_radius": value}
    elif operator == "values_count":
        return {"key": key, "values_count": value}
    return None


def create_filter_interface(metadata_keys: List[str]) -> Dict[str, List[Dict]]:
    """Create a comprehensive filter interface for Qdrant queries."""

    # Initialize session state for different filter types
    if "must_filters" not in st.session_state:
        st.session_state.must_filters = []
    if "must_not_filters" not in st.session_state:
        st.session_state.must_not_filters = []
    if "should_filters" not in st.session_state:
        st.session_state.should_filters = []

    # Create columns for filter type buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Add Must Filter"):
            st.session_state.must_filters.append(
                {"key": metadata_keys[0], "operator": "match", "value": ""}
            )
    with col2:
        if st.button("Add Must Not Filter"):
            st.session_state.must_not_filters.append(
                {"key": metadata_keys[0], "operator": "match", "value": ""}
            )
    with col3:
        if st.button("Add Should Filter"):
            st.session_state.should_filters.append(
                {"key": metadata_keys[0], "operator": "match", "value": ""}
            )

    filter_clause = {"must": [], "must_not": [], "should": []}

    # Create UI for Must filters
    if st.session_state.must_filters:
        st.subheader("Must Filters")
        for i, filter_item in enumerate(st.session_state.must_filters):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                with col1:
                    key = st.selectbox(
                        "Field",
                        metadata_keys,
                        key=f"must_key_{i}",
                        index=metadata_keys.index(filter_item["key"]),
                    )

                with col2:
                    operator = st.selectbox(
                        "Operator",
                        ["match", "range", "values_count"],
                        key=f"must_operator_{i}",
                    )

                with col3:
                    if operator == "match":
                        value = st.text_input("Value", key=f"must_value_{i}")
                    elif operator == "range":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input("Min", key=f"must_gte_{i}")
                        with col_max:
                            lte = st.number_input("Max", key=f"must_lte_{i}")
                        value = {"gte": gte, "lte": lte}
                    elif operator == "values_count":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input(
                                "Min Count", key=f"must_count_gte_{i}"
                            )
                        with col_max:
                            lte = st.number_input(
                                "Max Count", key=f"must_count_lte_{i}"
                            )
                        value = {"gte": gte, "lte": lte}

                with col4:
                    if st.button("Remove", key=f"remove_must_{i}"):
                        st.session_state.must_filters.pop(i)
                        st.rerun()

                filter_condition = create_filter_condition("must", key, operator, value)
                if filter_condition:
                    filter_clause["must"].append(filter_condition)

    # Create UI for Must Not filters
    if st.session_state.must_not_filters:
        st.subheader("Must Not Filters")
        for i, filter_item in enumerate(st.session_state.must_not_filters):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                with col1:
                    key = st.selectbox(
                        "Field",
                        metadata_keys,
                        key=f"must_not_key_{i}",
                        index=metadata_keys.index(filter_item["key"]),
                    )

                with col2:
                    operator = st.selectbox(
                        "Operator",
                        ["match", "range", "values_count"],
                        key=f"must_not_operator_{i}",
                    )

                with col3:
                    if operator == "match":
                        value = st.text_input("Value", key=f"must_not_value_{i}")
                    elif operator == "range":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input("Min", key=f"must_not_gte_{i}")
                        with col_max:
                            lte = st.number_input("Max", key=f"must_not_lte_{i}")
                        value = {"gte": gte, "lte": lte}
                    elif operator == "values_count":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input(
                                "Min Count", key=f"must_not_count_gte_{i}"
                            )
                        with col_max:
                            lte = st.number_input(
                                "Max Count", key=f"must_not_count_lte_{i}"
                            )
                        value = {"gte": gte, "lte": lte}

                with col4:
                    if st.button("Remove", key=f"remove_must_not_{i}"):
                        st.session_state.must_not_filters.pop(i)
                        st.rerun()

                filter_condition = create_filter_condition(
                    "must_not", key, operator, value
                )
                if filter_condition:
                    filter_clause["must_not"].append(filter_condition)

    # Create UI for Should filters
    if st.session_state.should_filters:
        st.subheader("Should Filters")
        for i, filter_item in enumerate(st.session_state.should_filters):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 3, 1])

                with col1:
                    key = st.selectbox(
                        "Field",
                        metadata_keys,
                        key=f"should_key_{i}",
                        index=metadata_keys.index(filter_item["key"]),
                    )

                with col2:
                    operator = st.selectbox(
                        "Operator",
                        ["match", "range", "values_count"],
                        key=f"should_operator_{i}",
                    )

                with col3:
                    if operator == "match":
                        value = st.text_input("Value", key=f"should_value_{i}")
                    elif operator == "range":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input("Min", key=f"should_gte_{i}")
                        with col_max:
                            lte = st.number_input("Max", key=f"should_lte_{i}")
                        value = {"gte": gte, "lte": lte}
                    elif operator == "values_count":
                        col_min, col_max = st.columns(2)
                        with col_min:
                            gte = st.number_input(
                                "Min Count", key=f"should_count_gte_{i}"
                            )
                        with col_max:
                            lte = st.number_input(
                                "Max Count", key=f"should_count_lte_{i}"
                            )
                        value = {"gte": gte, "lte": lte}

                with col4:
                    if st.button("Remove", key=f"remove_should_{i}"):
                        st.session_state.should_filters.pop(i)
                        st.rerun()

                filter_condition = create_filter_condition(
                    "should", key, operator, value
                )
                if filter_condition:
                    filter_clause["should"].append(filter_condition)

    # Display current filter structure
    if any([filter_clause["must"], filter_clause["must_not"], filter_clause["should"]]):
        st.subheader("Current Filter Structure")
        st.json(filter_clause)

    return filter_clause