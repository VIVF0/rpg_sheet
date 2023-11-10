import './TextInput.css'

const TextInput = (props) => {
    const whenTyped = (event) => {
        props.aoChanged(event.target.value)
    }
    return (
        <div className="campo-texto">
            <label>{props.label}</label>
            <input name={props.name} value={props.value} type={props.type} onChange={whenTyped} required={props.required} placeholder={props.placeholder}/>
        </div>
    )
}

export default TextInput