import streamlit as st
import pandas as pd

class PreemptivePrioritySchedulingDashboard:
    def __init__(self):
        if 'processes' not in st.session_state:
            st.session_state.processes = []

    def add_processes(self, num_processes):
        form_key = "add_processes_form_" + str(num_processes)
        with st.form(form_key):
            processes = []
            for i in range(num_processes):
                process_id = "P" + str(i+1)
                col1, col2, col3 = st.columns(3)
                with col1:
                    arrival_time = st.number_input("Arrival Time " + process_id, key=process_id + "_arrival_time", step=1)
                with col2:
                    burst_time = st.number_input("Burst Time " + process_id, key=process_id + "_burst_time", step=1)
                with col3:
                    priority = st.number_input("Priority " + process_id, key=process_id + "_priority", step=1)

                processes.append({
                    "id": process_id,
                    "arrival_time": arrival_time,
                    "burst_time": burst_time,
                    "priority": priority
                })

            submitted = st.form_submit_button("Add Processes")

            if submitted:
                st.session_state.processes.extend(processes)
                st.write("Processes added successfully!")

    def preemptive_priority_schedule(self):
        # Sort processes by arrival time
        st.session_state.processes.sort(key=lambda x: x["arrival_time"])

        # Initialize current time and total execution time
        current_time = 0
        total_execution_time = sum(process["burst_time"] for process in st.session_state.processes)

        # Create output data
        output_data = []

        total_turn_around_time = 0
        total_waiting_time = 0
        total_response_time = 0

        first_arrival_time = None

        while current_time < total_execution_time:
            available_processes = [process for process in st.session_state.processes if process["arrival_time"] <= current_time]

            if available_processes:
                # Select the process with the highest priority
                selected_process = min(available_processes, key=lambda x: x["priority"])

                # Calculate execution time (1 unit)
                execution_time = min(selected_process["burst_time"], 1)

                # Update burst time of the selected process
                selected_process["burst_time"] -= execution_time

                # Calculate completion time
                completion_time = current_time + execution_time

                # Calculate turn around time, waiting time, and response time
                turn_around_time = completion_time - selected_process["arrival_time"]
                waiting_time = turn_around_time - selected_process["burst_time"]
                response_time = selected_process["arrival_time"] - first_arrival_time if first_arrival_time is not None else 0

                # Update total turn around time, waiting time, and response time
                total_turn_around_time += turn_around_time
                total_waiting_time += waiting_time
                total_response_time += response_time

                # Add output data
                output_data.append({
                    "Time Instance": f"{current_time} ms - {completion_time} ms",
                    "Process": selected_process["id"],
                    "Arrival Time": f"{selected_process['arrival_time']} ms",
                    "Priority": selected_process["priority"],
                    "Execution Time": f"{execution_time} ms",
                    "Initial Burst Time": f"{selected_process['burst_time'] + execution_time} ms",
                    "Final Burst Time": f"{selected_process['burst_time']} ms"
                })

                # Update current time
                current_time = completion_time

                # Remove process if completed
                if selected_process["burst_time"] == 0:
                    st.session_state.processes.remove(selected_process)

                # Set the first arrival time
                if first_arrival_time is None:
                    first_arrival_time = selected_process["arrival_time"]
            else:
                # No process available, increment current time
                current_time += 1

        # Calculate averages
        num_processes = len(output_data)
        average_turn_around_time = total_turn_around_time / num_processes
        average_waiting_time = total_waiting_time / num_processes
        average_response_time = total_response_time / num_processes

        # Create output dataframe
        output_df = pd.DataFrame(output_data)

        # Display output dataframe
        st.write(output_df)

        # Display additional calculations
        st.write(f"Total Turn Around Time = {total_turn_around_time} ms")
        st.write(f"Average Turn Around Time = {average_turn_around_time:.2f} ms")
        st.write(f"Total Waiting Time = {total_waiting_time} ms")
        st.write(f"Average Waiting Time = {average_waiting_time:.2f} ms")
        st.write(f"Total Response Time = {total_response_time} ms")
        st.write(f"Average Response Time = {average_response_time:.2f} ms")

if __name__ == "__main__":
    st.title("Preemptive Priority Scheduling Dashboard")
    dashboard = PreemptivePrioritySchedulingDashboard()

    num_processes = st.number_input("Number of Processes:", step=1)

    if num_processes <= 0:
        st.error("Number of processes must be a positive integer")
    else:
        dashboard.add_processes(int(num_processes))

        if st.button("Run Preemptive Priority Scheduling Algorithm"):
            dashboard.preemptive_priority_schedule()
