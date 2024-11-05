/* Returns a date string in the format Weekday, Month Day, Year */

export const getCurrentFormattedDate = () => {
    return new Date().toLocaleString('en-CA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long',
    });
}