
def getInputsMenciones(id, menciones):

    text = ''
    for mencion in menciones:

        text += f"""
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="{id}" value="{mencion['id']}" id="{str(f"{id}-{mencion['nombre_abrev']}")}">
            <label class="form-check-label" for="{str(f"{id}-{mencion['nombre_abrev']}")}" title="{mencion['nombre']}">
                {mencion['nombre_abrev']}
            </label>
        </div>
        """
    return text