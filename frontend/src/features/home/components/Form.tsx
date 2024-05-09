/**
 * Handles submission of user input
 */

type FormProps = {
    name: string
    children: React.ReactNode
};

type FormState = {
    
};

export function Form({name, children}: FormProps) {

    function componentDidUpdate(prevProps: FormProps, prevState: FormState) {
        // Make network request
        // Update state with response
    };

    return (
        <>
        <div>{name}</div>
        {children}
        </>
    );
};