import { useQuery } from "react-query";

import { Building, BuildingsSchema } from "../../../types";

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

    const unvalidatedData = await response.json();
    const result = BuildingsSchema.safeParse(unvalidatedData);

    if (!result.success) {
        throw new Error(`Error in validation: ${result.error.format()}`);
    }

    return result.data;
}

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