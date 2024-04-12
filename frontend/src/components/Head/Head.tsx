/**
 * Contains the website title and other metadata
 */

type HeadProps = {
    title?: string,
    description?: string,
};

export function Head(props: HeadProps) {
    return (
        <>
            <title>{props.title? '${props.title}' : 'UBC Classrooms'}</title>
            <meta name='description'>{props.description? '${props.description}' : 'Space finder for UBC buildings'}</meta>
        </>
    );
};