/* Generates a time option array from startTime to endTime, with each value separated by an interval */
/* Assumes startTime and endTime end with ":00" or ":30" */
export const createTimeIntervals = (startTime: string, endTime: string, intervalMinutes: number): {value: string, label: string}[] => {
    const startDate = new Date(`2024-05-13 ${startTime}`); // used to take advantage of date operations
    const endDate = new Date(`2024-05-13 ${endTime}`);
    const timeArr = [];

    for (let currDate = startDate; currDate <= endDate; currDate.setTime(currDate.getTime() + intervalMinutes * 60000)) {
        const timeValueString = currDate.toLocaleTimeString('sv').slice(0, 5); // gets hour and minute portion only of 24 hour time format
        const timeLabelString = currDate.toLocaleTimeString('us').replace(/(:00\s)|(:30\s)/, " ") // formats the time into 12 hour AM/PM format for display

        timeArr.push({value: timeValueString, label: timeLabelString});
    }

    return timeArr;
};