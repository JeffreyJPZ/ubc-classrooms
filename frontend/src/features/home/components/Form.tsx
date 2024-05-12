/**
 * Handles submission of user input
 */

import { FormEvent } from 'react';
import './Form.css'

type FormProps = {
    children: React.ReactNode
};

type FormState = {
    
};

export function Form({children}: FormProps) {

    // function componentDidUpdate(prevProps: FormProps, prevState: FormState) {
    //     // Make network request
    //     // Update state with response
    // };

    function onSubmit(e: FormEvent) {
       console.log(e.target);
    }

    return (
        <div className="filters">
            {children}
            <button onClick={e => onSubmit(e)}>Search</button>
        </div>
    );
};