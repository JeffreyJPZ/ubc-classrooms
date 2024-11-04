import { useQuery } from "react-query";
import queryString from "query-string";

import { Timeslots, TimeslotsSchema } from "../../../types";
import { queryClient } from "../../../lib/react-query";

interface GetTimeslotQueryKeys {
    id: string,
    formSubmittedToggle: boolean
}

interface GetTimeslotParameters {
    campus: string,
    date: string,
    start?: string,
    end?: string,
    buildings?: string[],
    room_types?: string[],
};

type TransformedData = Record<string, Record<string, Timeslots>>;

const useTimeslotsConfig = {
    refetchOnWindowFocus: false,
    retry: true,
    useErrorBoundary: true,
};

async function getTimeslots(parameters: GetTimeslotParameters): Promise<Timeslots> {
    const queryParams = queryString.stringify(parameters, {skipEmptyString: true}).replace(`campus=${parameters.campus}`, "").replace(/%3A/g, ":");

    const response = await fetch(`/api/v1/timeslots/${parameters.campus}/?${queryParams}`, {
        headers: {
            "accepts":"application/json"
        }}
    );

    if (!response.ok) {
        throw new Error(`Response was not ok, received ${response.status}`);
    }

    const unvalidatedData = await response.json();
    const result = TimeslotsSchema.safeParse(unvalidatedData);

    if (!result.success) {
        throw new Error(`Error in validation: ${result.error.format()}`);
    }

    return result.data;
}

function mapTimeslotsToBuildingsAndRooms(data: Timeslots): TransformedData {
    return data.reduce((transformedData, currTimeslot) => {
        if (transformedData[currTimeslot.building_code] && transformedData[currTimeslot.building_code][currTimeslot.room]) {
            // entry for building and room exists
            transformedData[currTimeslot.building_code][currTimeslot.room].push(currTimeslot);
        } else if (transformedData[currTimeslot.building_code]) {
            // entry for building exists
            transformedData[currTimeslot.building_code][currTimeslot.room] = [currTimeslot];
        } else {
            // no entry for building exists
            const roomObj = {} as Record<string, Timeslots>;
            roomObj[currTimeslot.room] = [currTimeslot];
            transformedData[currTimeslot.building_code] = roomObj;
        }
        return transformedData;
    }, {} as TransformedData);
}

export const useTimeslots = (parameters: GetTimeslotParameters, keys: GetTimeslotQueryKeys) => {
    return useQuery({
        ...useTimeslotsConfig,
        // Refetches data only when form is submitted AND either campus or date has changed (most query data will be subset of initial loaded data)
        queryKey: [keys],
        queryFn: () => getTimeslots(parameters),
        // Returns data as timeslots mapped to buildings and room names matching query parameters
        select: mapTimeslotsToBuildingsAndRooms,
    });
};