import { useEffect, useState } from "react";
import { getCrops, getCounties } from "../services/api";

function PredictionForm({ onSubmit }) {

  const [crops, setCrops] = useState([]);
  const [counties, setCounties] = useState([]);

  const [formData, setFormData] = useState({
    crop: "",
    county: "",
    start_date: "",
    end_date: ""
  });


  useEffect(() => {

    async function loadOptions() {

      try {

        const cropsData = await getCrops();
        const countiesData = await getCounties();

        setCrops(cropsData);
        setCounties(countiesData);

      } catch (error) {

        console.error(
          "Error loading options:",
          error
        );

      }

    }

    loadOptions();

  }, []);



  function handleChange(e) {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  }



  function handleSubmit(e) {

    e.preventDefault();

    onSubmit(formData);

  }



  return (

    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow p-6 space-y-4 max-w-lg mx-auto"
    >


      <select
        name="crop"
        value={formData.crop}
        onChange={handleChange}
        className="w-full border rounded p-2"
        required
      >

        <option value="">
          Select Crop
        </option>

        {crops.map((crop) => (

          <option key={crop} value={crop}>
            {crop}
          </option>

        ))}

      </select>



      <select
        name="county"
        value={formData.county}
        onChange={handleChange}
        className="w-full border rounded p-2"
        required
      >

        <option value="">
          Select County
        </option>

        {counties.map((county) => (

          <option key={county} value={county}>
            {county}
          </option>

        ))}

      </select>



      <input
        type="date"
        name="start_date"
        value={formData.start_date}
        onChange={handleChange}
        className="w-full border rounded p-2"
        required
      />



      <input
        type="date"
        name="end_date"
        value={formData.end_date}
        onChange={handleChange}
        className="w-full border rounded p-2"
        required
      />



      <button
        type="submit"
        className="w-full bg-green-700 text-white py-2 rounded hover:bg-green-800"
      >

        Predict Yield

      </button>


    </form>

  );

}


export default PredictionForm;