from flask import Flask, request, render_template
from src.pipelines.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict_datapoints():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        data = CustomData(
            Line_Item_Quantity     = float(request.form.get("Line_Item_Quantity")),
            Pack_Price             = float(request.form.get("Pack_Price")),
            Weight_Kilograms       = float(request.form.get("Weight_Kilograms")),
            Unit_Price             = float(request.form.get("Unit_Price")),
            Brand                  = request.form.get("Brand"),
            Dosage_Form            = request.form.get("Dosage_Form"),
            Country                = request.form.get("Country"),
            Dosage                 = request.form.get("Dosage"),
            Item_Description       = request.form.get("Item_Description"),
            PO_SO                  = request.form.get("PO_SO"),
            )
            

        final_new_data = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)

        results=round(pred[0],2)

        return render_template('results.html',final_result=results)


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True,port=5001)