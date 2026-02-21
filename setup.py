from setuptools import setup, find_packages

setup(
    name="alphax_annual_leave_engine",
    version="0.1.0",
    description="Annual Leave deduction logic: calendar days (weekends included) minus selected public holidays.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
