import { useQuery } from "react-query";
import queryString from "query-string";

import { Timeslot } from "../../../types";

type GetTimeslotParameters = {
    campus: string,
    date: string,
    start?: string,
    end?: string,
    buildings?: string[],
    room_types?: string[],
};

async function getTimeslots(parameters: GetTimeslotParameters): Promise<Timeslot[]> {
    /* TODO: zod validation */

    /* Replaces empty arrays with undefined */
    if (!parameters.buildings) {
        parameters.buildings = undefined;
    }

    if (!parameters.room_types) {
        parameters.room_types = undefined;
    }

    const queryParams = queryString.stringify(parameters, {skipEmptyString: true}).replace(`campus=${parameters.campus}`, "").replace(/%3A/g, ":");

    const response = await fetch(`/api/v1/timeslots/${parameters.campus}/?${queryParams}`, {
        headers: {
            "accepts":"application/json"
        }}
    );

    if (!response.ok) {
        throw new Error(`Response was not ok, received ${response.status}`)
    }

    return response.json();
};

const useTimeslotsConfig = {
    refetchOnWindowFocus: false,
    retry: true,
    useErrorBoundary: true,
};

export const useTimeslots = (parameters: GetTimeslotParameters, keys: unknown[]) => {
    return useQuery({
        ...useTimeslotsConfig,
        // Refetches data only when given keys change
        queryKey: ["timeslots", ...keys],
        queryFn: () => getTimeslots(parameters),
    });
};