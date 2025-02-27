import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./SignUpForm.css";

const SignUpPage = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    if (touched[name]) {
      validateField(name, value);
    }
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;

    setTouched({
      ...touched,
      [name]: true,
    });

    validateField(name, value);
  };

  const validateField = (name, value) => {
    let error = "";

    switch (name) {
      case "firstName":
        error = !value.trim() ? "First name is required" : "";
        break;
      case "lastName":
        error = !value.trim() ? "Last name is required" : "";
        break;
      case "email":
        if (!value.trim()) {
          error = "Email is required";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          error = "Please enter a valid email address";
        }
        break;
      case "password":
        if (!value) {
          error = "Password is required";
        } else if (value.length < 8) {
          error = "Password must be at least 8 characters long";
        }
        break;
      case "confirmPassword":
        if (!value) {
          error = "Please confirm your password";
        } else if (value !== formData.password) {
          error = "Passwords do not match";
        }
        break;
      default:
        break;
    }

    setErrors((prev) => ({
      ...prev,
      [name]: error,
    }));

    return error === "";
  };

  const validateForm = () => {
    const fieldNames = [
      "firstName",
      "lastName",
      "email",
      "password",
      "confirmPassword",
    ];
    let isValid = true;

    const allTouched = {};
    fieldNames.forEach((field) => {
      allTouched[field] = true;
    });
    setTouched(allTouched);

    fieldNames.forEach((field) => {
      const valid = validateField(field, formData[field]);
      isValid = isValid && valid;
    });

    return isValid;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (validateForm()) {
      console.log("Form submitted successfully:", formData);

      setFormData({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: "",
      });

      setTouched({});
      setErrors({});

      alert("Sign up successful!");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form-container">
        <h1>Create an Account</h1>
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label
              htmlFor="firstName"
              className={errors.firstName ? "error-label" : ""}
            >
              {errors.firstName || "First Name"}
            </label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              onBlur={handleBlur}
              className={errors.firstName ? "error" : ""}
            />
          </div>

          <div className="form-group">
            <label
              htmlFor="lastName"
              className={errors.lastName ? "error-label" : ""}
            >
              {errors.lastName || "Last Name"}
            </label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              onBlur={handleBlur}
              className={errors.lastName ? "error" : ""}
            />
          </div>

          <div className="form-group">
            <label
              htmlFor="email"
              className={errors.email ? "error-label" : ""}
            >
              {errors.email || "Email"}
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              onBlur={handleBlur}
              className={errors.email ? "error" : ""}
            />
          </div>

          <div className="form-group">
            <label
              htmlFor="password"
              className={errors.password ? "error-label" : ""}
            >
              {errors.password || "Password"}
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              onBlur={handleBlur}
              className={errors.password ? "error" : ""}
            />
          </div>

          <div className="form-group">
            <label
              htmlFor="confirmPassword"
              className={errors.confirmPassword ? "error-label" : ""}
            >
              {errors.confirmPassword || "Confirm Password"}
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              onBlur={handleBlur}
              className={errors.confirmPassword ? "error" : ""}
            />
          </div>

          <button type="submit" className="auth-submit-btn">
            Sign Up
          </button>
        </form>

        <p className="auth-redirect">
          Already have an account? <Link to="/signin">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default SignUpPage;
