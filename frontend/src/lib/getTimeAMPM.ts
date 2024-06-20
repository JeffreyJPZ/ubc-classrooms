/* Returns a time string in 12 hour format, given a time string in 24 hour format */
/* Assumes the input string is in the form "XX:YY" where 0 <= XX <= 23 and YY is either 00 or 30 */

export const getTimeAMPM = (time: string) => {
    const date = new Date(`2024-05-13 ${time}`); // used to take advantage of date operations
    return date.toLocaleTimeString('us').replace(/(:00\s)|(:30\s)/, " ") // formats the time into 12 hour AM/PM format for display
}