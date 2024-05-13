import { useQuery } from "react-query";

import { RoomType } from "../../../types";

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

    return response.json();
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