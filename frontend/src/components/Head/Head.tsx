/**
 * Contains the website title and other metadata
 */

type HeadProps = {
    title?: string,
    description?: string,
};

function Head({title = '', description = ''}: HeadProps) {
    return (
        <>
            <title>{title? '${title}' : 'UBC Classrooms'}</title>
            <meta name='description'>{description? '${description}' : 'Space finder for UBC buildings'}</meta>
        </>
    );
};

export default Head