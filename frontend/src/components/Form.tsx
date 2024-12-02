import { useForm } from "react-hook-form";
import { FormProps } from "../types/FormType";

export default function Form({ onSubmit }: FormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<{
    patentId: string;
    companyName: string;
  }>();

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="w-full max-w-sm bg-white p-6 rounded-lg"
    >
      <div className="mb-4">
        <label
          htmlFor="patentId"
          className="text-left block text-sm font-medium text-gray-700"
        >
          Patent ID
        </label>
        <input
          id="patentId"
          type="text"
          placeholder="Enter Patent ID"
          {...register("patentId", { required: "Patent ID is required" })}
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
        />
        {errors.patentId && (
          <span className="text-red-500 text-sm">
            {errors.patentId.message}
          </span>
        )}
      </div>

      <div className="mb-4">
        <label
          htmlFor="companyName"
          className="text-left block text-sm font-medium text-gray-700"
        >
          Company Name
        </label>
        <input
          id="companyName"
          type="text"
          placeholder="Enter Company Name"
          {...register("companyName", { required: "Company Name is required" })}
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
        />
        {errors.companyName && (
          <span className="text-red-500 text-sm">
            {errors.companyName.message}
          </span>
        )}
      </div>

      <div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          Search Patent
        </button>
      </div>
    </form>
  );
}
