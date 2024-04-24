import streamlit as st
import pandas as pd

def lru_page_replacement(pages, capacity):
    cache = set()
    indexes = dict()
    page_faults = 0
    result = []

    for i, page in enumerate(pages):
        if len(cache) < capacity:
            if page not in cache:
                cache.add(page)
                indexes[page] = i
                page_faults += 1
            else:
                indexes[page] = i
        else:
            if page not in cache:
                lru_page = min(indexes, key=indexes.get)
                cache.remove(lru_page)
                cache.add(page)
                indexes.pop(lru_page)
                indexes[page] = i
                page_faults += 1
            else:
                indexes[page] = i

        result.append((i+1, page, ", ".join(map(str, cache)), page_faults))

    result.append(("Total", "", "", page_faults))
    return result

def main():
    st.title("LRU Page Replacement Algorithm Dashboard")
    st.sidebar.header("Settings")
    capacity = st.sidebar.number_input("Cache Capacity", min_value=1, step=1, value=4)
    input_pages = st.text_area("Enter page requests separated by comma (e.g., 7,0,1,2,0,3,0,4,2,3,0,3,2)")

    if st.button("Run Algorithm"):
        pages = [int(page) for page in input_pages.split(",")]
        result = lru_page_replacement(pages, capacity)
        df = pd.DataFrame(result, columns=["Operation", "Page Request", "Cache Memory", "Fault Count"])
        st.write(df)

if __name__ == "__main__":
    main()
