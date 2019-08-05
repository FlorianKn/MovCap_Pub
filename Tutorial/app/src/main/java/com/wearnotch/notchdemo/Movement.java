package com.wearnotch.notchdemo;

import java.util.ArrayList;
import java.util.List;

public class Movement {
    private ArrayList<Float> ElbowFlexion;
    private ArrayList<Float> ElbowSupination;
    private ArrayList<Float> ShoulderFlexion;
    private ArrayList<Float> ShoulderAbduction;

    public ArrayList<Float> getShoulderRotation() {
        return ShoulderRotation;
    }

    private ArrayList<Float> ShoulderRotation;


    public Movement(ArrayList<Float> elbowFlexion, ArrayList<Float> elbowSupination, ArrayList<Float> shoulderFlexion, ArrayList<Float> shoulderAbduction, ArrayList<Float> shoulderRotation) {
        ElbowFlexion = elbowFlexion;
        ElbowSupination = elbowSupination;
        ShoulderFlexion = shoulderFlexion;
        ShoulderAbduction = shoulderAbduction;
        ShoulderRotation = shoulderRotation;
    }

    public List<Float> getElbowFlexion() {
        return ElbowFlexion;
    }

    public List<Float> getElbowSupination() {
        return ElbowSupination;
    }

    public List<Float> getShoulderFlexion() {
        return ShoulderFlexion;
    }

    public List<Float> getShoulderAbduction() {
        return ShoulderAbduction;
    }
}
