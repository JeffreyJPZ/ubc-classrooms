import { useQuery } from "react-query";

import { Building } from "../../../types";

type GetBuildingsParameters = {
    campus: "UBCV",
};

async function getBuildings(parameters: GetBuildingsParameters): Promise<Building[]> {
    const response = await fetch(`/api/v1/buildings/${parameters.campus}`, {
        headers: {
            "accepts":"application/json"
        }}
    );
    
    if (!response.ok) {
        throw new Error(`Response was not ok, received ${response.status}`)
    }

    return response.json();
};

const useBuildingsConfig = {
    refetchOnWindowFocus: false,
    retry: true,
    useErrorBoundary: true,
};

export const useBuildings = (parameters: GetBuildingsParameters) => {
    return useQuery({
        ...useBuildingsConfig,
        queryKey: ["buildings"],
        queryFn: () => getBuildings(parameters),
    });
};