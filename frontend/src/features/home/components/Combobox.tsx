import Select, { MultiValue, SingleValue } from 'react-select';
import { UseQueryResult } from 'react-query';

import './Combobox.css';

export type Option = {value: string, label: string};
export type Options = SingleValue<{value: string, label: string}> | MultiValue<{value: string, label: string}>;
export type OptionsEventHandler = (arg0: Options) => void;
type OptionsT = Record<string, string>[];
type QueryT = UseQueryResult<Record<string, string>[], unknown>;

type ComboboxProps = {
    required?: boolean,
    isMulti?: boolean,
    isClearable?: boolean,
    defaultValue?: string,
    defaultLabel?: string,
    options?: OptionsT,
    optionValue?: string,
    optionLabel?: string,
    query?: QueryT | null,
    queryValue?: string,
    queryLabel?: string,
    onChange?: OptionsEventHandler,
}

export function Combobox({required = false, isMulti = false, isClearable = true, defaultValue = "", defaultLabel = "", options = [], optionValue = "", optionLabel = "", query = null, queryValue = "", queryLabel = "", onChange = () => {}}: ComboboxProps) {
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
            return (
                <Select className="combobox" required={required} isMulti={isMulti} isClearable={isClearable} onChange={onChange} options={query.data.map(queryItem => {
                    return {value: queryItem[queryValue], label: queryItem[queryLabel]};
                })}/>
            );
        } else {
            return (
                <Select className="combobox" required={required} isMulti={isMulti} isClearable={isClearable} onChange={onChange} options={query.data.map(queryItem => {
                    return {value: queryItem[queryValue], label: `${queryItem[queryLabel]} (${queryItem[queryValue]})`};
                })}/>
            );
        }
    };

    if (required) {
        return (
            <Select className="combobox" required={required} defaultValue={{value: defaultValue, label: defaultLabel}} isMulti={isMulti} isClearable={isClearable} onChange={onChange} options={options.map(option => {
                return {value: option[optionValue], label: option[optionLabel]};
            })}/>
        );
    }

    return (
        <Select className="combobox" required={required} isMulti={isMulti} isClearable={isClearable} onChange={onChange} options={options.map(option => {
            return {value: option[optionValue], label: option[optionLabel]};
        })}/>
    );
    
    
};