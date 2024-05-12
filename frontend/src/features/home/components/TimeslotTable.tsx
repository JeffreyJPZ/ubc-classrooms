import { useBuildings } from "../api/getBuildings";

export function TimeslotTable() {
    const buildingsQuery = useBuildings({campus: "UBCV"});

    if (buildingsQuery.isLoading) {
        return (
            <div>Loading...</div>
        );
    };
    
    if (!buildingsQuery.data) {
        return (
            <div>Nothing to show...</div>
        );
    };

    return (
        <>
            {buildingsQuery.data.map((building) => {
                return (
                    <li key={building.building_code}>
                        <p>{building.building_code} - {building.building_name}</p>
                    </li>
                );
            })};
        </>
    );
};