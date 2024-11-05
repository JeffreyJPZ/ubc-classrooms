/* Generates a date option array with ISO 8601 values and labels in the format Weekday, Month Day, Year for a given number of days */
export const createISOAndFormattedDates = (startDate: string, days: number): {value: string, label: string}[] => {
    const currDate = new Date(startDate);
    const dateArr = [];

    for (let i = 0; i < days; i++) {
        currDate.setDate(currDate.getDate() + 1); // takes start date into account
        const value = currDate.toLocaleDateString('sv');
        const label = currDate.toLocaleDateString('en-CA', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long',
        });
        dateArr.push({value: value, label: label});
    }

    return dateArr;
};