/* Generates a date option array in ISO 8601 format for a given number of days*/
export const createISODates = (startDate: string, days: number): {value: string, label: string}[] => {
    const currDate = new Date(startDate);
    const dateArr = [];

    for (let i = 0; i < days; i++) {
        currDate.setDate(currDate.getDate() + 1); // takes start date into account
        const dateString = currDate.toLocaleDateString('sv');
        dateArr.push({value: dateString, label: dateString});
    }

    return dateArr;
};