import streamlit as st
import matplotlib.pyplot as plt

def fcfs_disk_scheduling(initial_head, requests):
    total_seek_count = 0
    sequence = []

    current_track = initial_head
    sequence.append(initial_head)
    for request in requests:
        seek_count = abs(request - current_track)
        total_seek_count += seek_count
        current_track = request
        sequence.append(request)

    return total_seek_count, sequence

def main():
    st.title("FCFS Disk Scheduling Algorithm")

    # Input fields
    initial_head = st.number_input("Enter initial head position:", value=0, step=1)
    requests_text = st.text_area("Enter list of requests separated by commas (e.g., 98,183,37,122,14,124,65,67):")

    if st.button("Run FCFS"):
        try:
            requests = [int(x.strip()) for x in requests_text.split(',')]
            seek_count, sequence = fcfs_disk_scheduling(initial_head, requests)

            # Display total seek count
            st.write("Total Seek Count:", seek_count)

            # Plot the sequence
            plt.figure(figsize=(10, 5))
            plt.plot(range(len(sequence)), sequence, marker='o')
            plt.title("FCFS Disk Scheduling Sequence")
            plt.xlabel("Request")
            plt.ylabel("Track")
            plt.xticks(range(len(sequence)), sequence)  # Set track numbers as ticks
            plt.axhline(y=initial_head, color='r', linestyle='--', label='Initial Head')  # Add line for initial head
            plt.legend()
            for i, txt in enumerate(sequence):
                plt.annotate(txt, (i, sequence[i]), xytext=(-8, 8), textcoords='offset points')
            st.pyplot(plt)

        except ValueError:
            st.error("Invalid input. Please enter valid integers separated by commas.")

if __name__ == "__main__":
    main()
