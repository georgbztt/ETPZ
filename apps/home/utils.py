
def getInputsMenciones(id, menciones, data=None):

    text = ''
    for mencion in menciones:
 
        checked = ""

        if data != None:
            for i in data:
                if (mencion['id'] == i.mencion.id) and (id == i.anio.id):
                    checked = "checked"
        

        text += f"""
        <div class="form-check">
            <input class="form-check-input" type="checkbox" name="{id}" value="{mencion['id']}" id="{str(f"{id}-{mencion['nombre_abrev']}")}" {checked}>
            <label class="form-check-label" for="{str(f"{id}-{mencion['nombre_abrev']}")}" title="{mencion['nombre']}">
                {mencion['nombre_abrev']}
            </label>
        </div>
        """
    return text