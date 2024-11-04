import { forwardRef } from "react";
import { ForwardedMapRef } from "../../../types";

import "./MapContainer.css";

type MapContainerProps = {};

export const MapContainer = forwardRef(function MapContainer(props: MapContainerProps, ref: ForwardedMapRef<HTMLDivElement | null>): JSX.Element {
    return (
        <div className="map-container" {...props} ref={ref}/>
    );
});