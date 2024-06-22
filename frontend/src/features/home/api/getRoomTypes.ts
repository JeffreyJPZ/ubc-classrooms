import { useQuery } from "react-query";

import { RoomType, RoomTypesSchema } from "../../../types";

type GetRoomTypesParameters = {
    campus: "UBCV",
};

async function getRoomTypes(parameters: GetRoomTypesParameters): Promise<RoomType[]> {
    const response = await fetch(`/api/v1/roomtypes/${parameters.campus}`, {
        headers: {
            "accepts":"application/json"
        }}
    );
    
    if (!response.ok) {
        throw new Error(`Response was not ok, received ${response.status}`)
    }

    const unvalidatedData = await response.json();
    const result = RoomTypesSchema.safeParse(unvalidatedData);

    if (!result.success) {
        throw new Error(`Error in validation: ${result.error.format()}`);
    };

    return result.data;
};

const useRoomTypesConfig = {
    refetchOnWindowFocus: false,
    retry: true,
    useErrorBoundary: true,
};

export const useRoomTypes = (parameters: GetRoomTypesParameters) => {
    return useQuery({
        ...useRoomTypesConfig,
        queryKey: ["roomtypes"],
        queryFn: () => getRoomTypes(parameters),
    });
};