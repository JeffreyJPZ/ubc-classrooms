import { useQuery } from "react-query";
import queryString from "query-string";

import { Timeslot } from "../../../types";

type GetTimeslotParameters = {
    campus: "UBCV",
    buildings?: string[],
    room_types?: string[],
    date: string,
    start?: string,
    end?: string,
};

async function getTimeslots(parameters: GetTimeslotParameters): Promise<Timeslot[]> {
    let queryParams = queryString.stringify(parameters).replace(`&campus=${parameters.campus}`, "");

    const response = await fetch(`/api/v1/timeslots/${parameters.campus}/?${queryParams}`, {
        headers: {
            "accepts":"application/json"
        }}
    );
    if (!response.ok) {
        throw new Error(`Response was not ok, received ${response.status}`)
    }
    return await response.json();
};

const useTimeslotsConfig = {
    refetchOnWindowFocus: false,
    retry: true,
    useErrorBoundary: true,
};

export const useTimeslots = (params: GetTimeslotParameters) => {
    return useQuery({
        ...useTimeslotsConfig,
        queryKey: ["timeslots"],
        queryFn: () => getTimeslots(params),
    });
};