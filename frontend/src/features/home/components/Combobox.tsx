import Select from 'react-select';
import { useBuildings } from '../api/getBuildings';
import { UseQueryResult } from 'react-query';

import './Combobox.css';

type QueryT = UseQueryResult<Record<string, string>[], unknown>

type ComboboxProps = {
    isMulti?: boolean,
    defaultValue?: string,
    defaultLabel?: string,
    options?: Record<string, string>[],
    optionValue?: string,
    optionLabel?: string,
    query?: QueryT | null,
    queryValue?: string,
    queryLabel?: string,
}

export function Combobox({isMulti = false, defaultValue = "", defaultLabel = "", options = [], optionValue = "", optionLabel = "", query = null, queryValue = "", queryLabel = ""}: ComboboxProps) {
    if (query && queryValue && queryLabel) {
        if (query.isLoading) {
            return (
                <div>Loading...</div>
            );
        };
        
        if (!query.data) {
            return (
                <div>Nothing to show...</div>
            );
        };
    
        if (queryValue === queryLabel) {
            return (<Select className="combobox" isMulti={isMulti} options={query.data.map(queryItem => {
                        return {value: queryItem[queryValue], label: queryItem[queryLabel]};
                    })}/>
            );
        } else {
            return (<Select className="combobox" isMulti={isMulti} options={query.data.map(queryItem => {
                return {value: queryItem[queryValue], label: `${queryItem[queryValue]} - ${queryItem[queryLabel]}`};
            })}/>
            );
        }
    }

    return (
        <>
            <Select className="combobox" defaultValue={{value: defaultValue, label: defaultLabel}} isMulti={isMulti} options={options.map(option => {
                return {value: option[optionValue], label: option[optionLabel]};
            })}/>
        </>
    );
    
};