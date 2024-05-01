/**
 * Handles submission of user input
 */

type FormProps = {
    name: string
    children: React.ReactNode
}

type FormState = {
    
}

export function Form(props: FormProps) {

    function componentDidUpdate(prevProps: FormProps, prevState: FormState) {
        // Make network request
        // Update state with response
    }

    return (
        <>
        <div>{props.name}</div>
        {props.children}
        </>
    )
}